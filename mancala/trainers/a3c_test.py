import datetime
from datetime import date
import time
from collections import deque

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from tensorboard_logger import configure, log_value

from mancala.env import MancalaEnv
from mancala.agents.random import AgentRandom
from mancala.agents.exact import AgentExact
from mancala.agents.max_min import AgentMinMax
from mancala.agents.a3c import AgentA3C
from mancala.arena import Arena
from mancala.trainers.a3c_model import ActorCritic


evaluation_episodes = 100


def test(rank, args, shared_model, dtype):
    test_ctr = 0
    torch.manual_seed(args.seed + rank)

    # set up logger
    timestring = str(date.today()) + '_' + \
        time.strftime("%Hh-%Mm-%Ss", time.localtime(time.time()))
    run_name = args.save_name + '_' + timestring
    configure("logs/run_" + run_name, flush_secs=5)

    env = MancalaEnv(args.seed + rank)
    env.seed(args.seed + rank)
    state = env.reset()

    model = ActorCritic(state.shape[0], env.action_space).type(dtype)

    model.eval()

    state = torch.from_numpy(state).type(dtype)
    reward_sum = 0
    max_reward = -99999999
    max_winrate = 0
    rewards_recent = deque([], 100)
    done = True

    start_time = time.time()
    last_test = time.time()

    episode_length = 0
    while True:
        episode_length += 1
        # Sync with the shared model
        if done:
            model.load_state_dict(shared_model.state_dict())
            cx = Variable(torch.zeros(1, 300).type(dtype), volatile=True)
            hx = Variable(torch.zeros(1, 300).type(dtype), volatile=True)
        else:
            cx = Variable(cx.data.type(dtype), volatile=True)
            hx = Variable(hx.data.type(dtype), volatile=True)

        value, logit, (hx, cx) = model(
            (Variable(state.unsqueeze(0), volatile=True), (hx, cx)))
        prob = F.softmax(logit)
        action = prob.max(1)[1].data.cpu().numpy()

        state, reward, done, _ = env.step(action[0, 0])
        done = done or episode_length >= args.max_episode_length
        reward_sum += reward

        if done:
            rewards_recent.append(reward_sum)
            rewards_recent_avg = sum(rewards_recent) / len(rewards_recent)
            print(
                "{} | {} | Episode Reward {: >4}, Length {: >2} | Avg Reward {:0.2f}".format(
                    datetime.datetime.now().isoformat(),
                    time.strftime("%Hh %Mm %Ss",
                                  time.gmtime(time.time() - start_time)),
                    round(reward_sum, 2),
                    episode_length,
                    round(rewards_recent_avg, 2))
            )

            # if not stuck or args.evaluate:
            log_value('Reward', reward_sum, test_ctr)
            log_value('Reward Average', rewards_recent_avg, test_ctr)
            log_value('Episode length', episode_length, test_ctr)

            if reward_sum >= max_reward or \
                time.time() - last_test > 60 * 8 or \
                (len(rewards_recent) > 12 and \
                    time.time() - last_test > 60 * 2 and \
                    sum(list(rewards_recent)[-5:]) > sum(list(rewards_recent)[-10:-5])):

                    # if the reward is better or every 15 minutes
                last_test = time.time()
                max_reward = reward_sum if reward_sum > max_reward else max_reward

                path_output = args.save_name + '_max'
                torch.save(shared_model.state_dict(), path_output)
                path_now = "{}_{}".format(
                    args.save_name, datetime.datetime.now().isoformat())
                torch.save(shared_model.state_dict(), path_now)

                win_rate_v_random = Arena.compare_agents_float(
                    lambda seed: AgentA3C(path_output, dtype, seed),
                    lambda seed: AgentRandom(seed),
                    400)
                win_rate_v_exact = Arena.compare_agents_float(
                    lambda seed: AgentA3C(path_output, dtype, seed),
                    lambda seed: AgentExact(seed),
                    400)
                win_rate_v_minmax = Arena.compare_agents_float(
                    lambda seed: AgentA3C(path_output, dtype, seed),
                    lambda seed: AgentMinMax(seed, 3),
                    400)
                msg = " {} | VsRandom: {: >4}% | VsExact: {: >4}% | VsMinMax: {: >4}%".format(
                    datetime.datetime.now().strftime("%c"),
                    round(win_rate_v_random * 100, 2),
                    round(win_rate_v_exact * 100, 2),
                    round(win_rate_v_minmax * 100, 2)
                )
                print(msg)
                log_value('WinRate_Random', win_rate_v_random, test_ctr)
                log_value('WinRate_Exact', win_rate_v_exact, test_ctr)
                log_value('WinRate_MinMax', win_rate_v_minmax, test_ctr)
                avg_win_rate = (win_rate_v_exact + win_rate_v_minmax) / 2
                if avg_win_rate > max_winrate:
                    print("Found superior model at {}".format(
                        datetime.datetime.now().isoformat()))
                    torch.save(shared_model.state_dict(), "{}_{}_best_{}".format(
                        args.save_name, datetime.datetime.now().isoformat(), avg_win_rate))
                    max_winrate = avg_win_rate

            reward_sum = 0
            episode_length = 0
            state = env.reset()
            test_ctr += 1

            if test_ctr % 10 == 0 and not args.evaluate:
                # pickle.dump(shared_model.state_dict(), open(args.save_name + '.p', 'wb'))
                torch.save(shared_model.state_dict(), args.save_name)
            if not args.evaluate:
                time.sleep(60)
            elif test_ctr == evaluation_episodes:
                # Ensure the environment is closed so we can complete the
                # submission
                env.close()
                # gym.upload('monitor/' + run_name, api_key=api_key)

        state = torch.from_numpy(state).type(dtype)

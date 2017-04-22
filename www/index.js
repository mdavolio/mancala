var board_current = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0];
var player_turn = 1;
const reset_state = () => {
  board_current = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0];
  player_turn = 1;
}

const player_types = { 'human': { url: '' }, 'random': { url: '' }, 'max': { url: '' },'exact': { url: '' }, 'min_max':{ url: '' } };
const players = ['one', 'two'];
var player_states = ['human', 'human'];

const human_turn = () => player_states[player_turn - 1] == 'human';

const update_progress = (player, agent, status, ms = 500) => {
  return new Promise((resolve, reject) => {
    $(`#progress-${player == 1 ? 'one' : 'two'}-${agent}`).velocity({
      width: `${status}%`
    }, {
        duration: ms,
        easing: "easeInOutCubic",
        complete: () => {
          resolve();
        }
      });
  });
};

const speed_slider = document.getElementById("agent_speed");
const count_down_progress = (player, agent) => {
  const value = 500 - speed_slider.value;
  return update_progress(player, agent, 100, value)
    .then(x => update_progress(player, agent, 0, value * 1.4))
}

const generate_inputs = (player, types) => {
  return R.pipe(
    R.mapObjIndexed((val, type) =>
      `<div class="pure-g">
         <div class="pure-u-1-6 center">
            <input id="option-${player}-${type}"
            type="radio"
            name="option-${player}"
            value="${type}"
            ${type == "human" ? "checked" : ""} />
        </div>
        <div class="pure-u-1-3">
          <p class="player-label">${type}</p>
        </div>
        <div class="pure-u-1-2 progress-container">
          <div id="progress-${player}-${type}" class="progress-bar"></div>
        </div>
      </div>
           `
    ),
    R.values,
    R.join('\n'),
    html => `${html}`
  )(types);
};

R.map((player) => {
  $(`#player_${player}_choices`).html(generate_inputs(player, player_types));
}, players);

var latest_url = '';
const fetch = (url) => {
  latest_url = url;
  return new Promise((resolve, reject) => {
    $.ajax({
      url,
      error: reject,
      success: (data) => {
        if (url != latest_url) {
          reject(false);
        } else {
          resolve(data);
        }
      }
    });
  });
};

const update_state_on_response = (e) => {
  if (!e) {
    return;
  }
  board_current = e.board;
  player_turn = e.player_turn;
  render_player(e);
  render_board(board_current);
  return !e.game_over;
};

const get_move = (url) => {
  return fetch(url)
    .catch(e => {
      if (e === false) {
        console.log('Caught failure');
        return false;
      }
      console.error(e);
      $('#server-message').html(e.responseJSON.error);
      return false;
    })
}

const cell_click = move => {
  if (!human_turn()) {
    console.log('Ignoring click');
    return;
  }
  // Send request
  return get_move(`/play/${board_to_str(board_current)}/${player_turn}/${move}`)
    .then(update_state_on_response)
    .then(kick_again);
};

const pulse_score = (elm, color = "#000000", fontSize = '100%', duration = 500) => {
  return new Promise((resolve, reject) => {
    elm.velocity({
      color,
      fontSize
    }, {
        duration,
        easing: "easeInOutCubic",
        complete: () => {
          resolve();
        }
      });
  });
};

const player_color = is_player_one => is_player_one ? 'rgba(33, 174, 255, 0.93)' : 'rgba(255, 0, 0, 0.93)';
const player_color_hex = is_player_one => is_player_one ? '#21aeff' : '#ff0000';

const player_one_score = $('#player_one_score');
const player_two_score = $('#player_two_score');
const auto_restart = $('#auto-restart');
const render_player = (game_state) => {
  const turn_elm = $('#player_turn');
  if (game_state.game_over) {
    const player_one_win = game_state.score[0] > game_state.score[1];
    const player_elm = player_one_win ? player_one_score : player_two_score;
    player_elm.html(+player_elm.html() + 1);
    turn_elm.html(`Player ${player_one_win ? 'One' : 'Two'} Wins!`);
    turn_elm.css('color', player_color(player_one_win));

    const player_scoreboard = player_one_win ? player_one_score : player_two_score;
    pulse_score(player_scoreboard, player_color_hex(player_one_win), '200%')
      .then(x => pulse_score(player_scoreboard))

    if (auto_restart.prop('checked')) {
      restart_game();
    }
  } else {
    turn_elm.html(`Player ${game_state.player_turn == 1 ? 'One' : 'Two'}'s Turn`);
    turn_elm.css('color', player_color(game_state.player_turn == 1));
  }
}

const i_to_str = i => i >= 10 ? `${i}` : `0${i}`;
const board_to_str = R.pipe(
  R.map(i_to_str),
  R.join('')
);
const over_cells = (cb) => {
  R.pipe(
    R.range(0),
    R.forEach(cb)
  )(14);
};
const render_cell = R.pipe(
  R.repeat(`⚫`),
  R.join('')
);
const cell_from_id = i => $(`#cell-${i_to_str(i)}`);
const render_board = (board) => over_cells(i => cell_from_id(i).html(render_cell(board[i])));
over_cells(i => cell_from_id(i).on('touchstart click', evt => cell_click(i)));


const kick_again = (again) => {
  if (again) {
    kick_turn();
  }
}
const kick_turn = () => {
  // if human, do nothing (wait for click)
  if (human_turn()) {
    return;
  }
  // if not human, kick off the paired wait, of move request/slide down
  // console.log(`Computer's turn!`);
  Promise.all([
    get_move(`/agent/${board_to_str(board_current)}/${player_turn}/${player_states[player_turn - 1]}`),
    count_down_progress(player_turn, player_states[player_turn - 1])
  ])
    .then(R.nth(0))
    .then(update_state_on_response)
    .then(kick_again);
}

$(`#btn-restart-game`).on('touchstart click', evt => {
  console.log('Restart Game');
  evt.preventDefault();
  restart_game();
});
const restart_game = () => {
  reset_state();
  render_board(board_current);
  render_player({ game_over: false, player_turn });

  const player_one_type = $("input[name=option-one]:checked").val();
  const player_two_type = $("input[name=option-two]:checked").val();
  player_states = [player_one_type, player_two_type];
  kick_turn();
}

render_board(board_current);
render_player({ game_over: false, player_turn });

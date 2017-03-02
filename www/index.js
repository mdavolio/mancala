var board_current = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0];
var player_turn = 1;
const player_types = { 'human': { url: '' }, 'random': { url: '' } };
const players = ['one', 'two'];
var player_states = ['human', 'human'];

const generate_inputs = (player, types) => {
  return R.pipe(
    R.mapObjIndexed((val, type) =>
      `<div class="pure-g">
         <div class="pure-u-1-3 radio-parent">
            <input id="option-${player}-${type}"
            type="radio"
            name="option-${player}"
            value="${type}"
            ${type == "human" ? "checked" : ""} />
        </div>
        <div class="pure-u-2-3">
          <p class="player-label">${type}</p>
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

const cell_click = move => {
  console.log(`Click ${move}`);
  $.ajax({
    url: `/play/${board_to_str(board_current)}/${player_turn}/${move}`,
    error: e => {
      console.error(e);
      $('#server-message').html(e.responseJSON.error);
    },
    success: (e) => {
      board_current = e.board;
      player_turn = e.player_turn;
      console.log(e);
      render_player(player_turn);
      render_board(board_current);
    }
  });
};
const render_player = (turn) => {
  const turn_elm = $('#player_turn');
  turn_elm.html(`Player ${player_turn == 1 ? 'One' : 'Two'}'s Turn`);
  turn_elm.css('color', player_turn == 1 ? 'rgba(33, 174, 255, 0.93)' : 'rgba(255, 0, 0, 0.93)');
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
const cell_from_id = i => $(`#cell-${i_to_str(i)}`);
const render_board = (board) => over_cells(i => cell_from_id(i).html(board[i] > 0 ? board[i] : ''));
over_cells(i => cell_from_id(i).on('touchstart click', evt => cell_click(i)));


$(`#btn-restart-game`).on('touchstart click', evt => {
  console.log('Restart Game');
  const player_one_type = $("input[name=option-one]:checked").val();
  const player_two_type = $("input[name=option-two]:checked").val();
});

render_board(board_current);
render_player(player_turn);

var board_current = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0];
var player_turn = 1;

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
      render_board(board_current);
    }
  });
};

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
const render_board = (board) => over_cells(i => cell_from_id(i).html(board[i]));
over_cells(i => cell_from_id(i).on('touchstart click', evt => cell_click(i)));

render_board(board_current);

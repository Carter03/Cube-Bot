function vis(cube) {
  const sc = 15; // scale factor = length of each sticker in pixels.
  const canvas = DOM.canvas(13 * sc, 10 * sc);
  const ctx = canvas.getContext('2d');
  
  // Retina display hacks
  scaleCanvas(canvas, ctx)
  ctx.translate(sc / 2, sc / 2)
  
  function draw(idx, r, c) {
    for (let i = r; i <= r + 2; i++)
      for (let j = c; j <= c + 2; j++) {
          ctx.fillStyle = color[cube[idx++]];
          ctx.fillRect(sc * j, sc * i, sc, sc);
          ctx.lineWidth = 2
          ctx.strokeRect(sc * j, sc * i, sc, sc)
      }
  }
  
  // draw the faces
  draw( 0, 0, 3) // U
  draw( 9, 3, 6) // R
  draw(18, 3, 3) // F
  draw(27, 6, 3) // D
  draw(36, 3, 0) // L
  draw(45, 3, 9) // B
  
  return canvas
}

perm_from_cycle = ƒ(cycle)
scaleCanvas = ƒ(canvas, ctx)

u_move = 
  [
    perm_from_cycle( [ S("U",1), S("U",3), S("U",9), S("U",7) ] ),
    perm_from_cycle( [ S("U",2), S("U",6), S("U",8), S("U",4) ] ),
    perm_from_cycle( [ S("F",1), S("L",1), S("B",1), S("R",1) ] ),
    perm_from_cycle( [ S("F",2), S("L",2), S("B",2), S("R",2) ] ),
    perm_from_cycle( [ S("F",3), S("L",3), S("B",3), S("R",3) ] ),
  ].flat()

apply_move = function(cube, perm) {
  let new_cube = [...cube]
  for (let x of perm) {
    new_cube[x[1]] = cube[x[0]]
  }
  //perm.forEach( ([src, dst]) => new_cube[dst] = cube[src] );
  return new_cube
}

vis(apply_move(solved_cube, u_move))

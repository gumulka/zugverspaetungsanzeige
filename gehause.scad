
frontside();

$fn = 40;

translate([ 0, -3, -1.5 ]) waveshare_7in5(false);

translate([ 13, -20, -5 ]) rotate([ 0, 180, 90 ]) waveshare_esp32_driver(false);

translate([ 0, 0, 1 ]) backplate();

module backplate() {
  difference() {
    union() {
      {
        translate([ 0, 0, -12 ]) linear_extrude(2) polygon([
          [ 10, 10 ],     [ 10, 54 ], // top left
          [ 3, 54 ],      [ 3, 48 ],      [ -3, 48 ],   [ -3, 54 ],
          [ -10, 54 ],    [ -10, 10 ], //  end of zunge
          [ -50.5, -10 ], [ -50.5, -66 ], [ -15, -66 ], [ 50.5, -66 ],
          [ 50.5, -50 ],  [ 40, -50 ],    [ 40, -56 ],  [ -15, -56 ],
          [ -15, -45 ],   [ -30, -45 ],   [ -30, -24 ], [ -15, -24 ],
          [ -15, -18 ],   [ 5, -18 ],     [ 5, -24 ],   [ 14, -24 ],
          [ 14, -18 ],
        ]);
        translate([ 0, 0, -10 ]) linear_extrude(4) polygon([
          [ -50.5, -50 ],
          [ -50.5, -66 ],
          [ -40, -66 ],
          [ -40, -50 ],
        ]);
        translate([ 0, 0, -10 ]) linear_extrude(4) polygon([
          [ 50.5, -50 ],
          [ 50.5, -66 ],
          [ 40, -66 ],
          [ 40, -50 ],
        ]);
        translate([ 0, 0, -6 ]) linear_extrude(3) polygon([
          [ -50.5, -50 ],
          [ -50.5, -58 ],
          [ -40, -58 ],
          [ -40, -50 ],
        ]);
        translate([ 0, 0, -6 ]) linear_extrude(3) polygon([
          [ 50.5, -50 ],
          [ 50.5, -58 ],
          [ 40, -58 ],
          [ 40, -50 ],
        ]);
      }
    }
    translate([ -44.5, -64, 0 ]) cylinder(h = 40, r = 1.5, center = true);
    translate([ 44.5, -64, 0 ]) cylinder(h = 40, r = 1.5, center = true);
    translate([ 44.5, -64, -11 ]) cylinder(h = 2.001, r = 3, center = true);
    translate([ -44.5, -64, -11 ]) cylinder(h = 2.001, r = 3, center = true);
  }
}

module frontside(top_bezel = 10, bottom_bezel = 22, side_bezels = 10,
                 wall_thickness = 2.5, depth = 13, front_thickness = 1) {

  viewport_width = 158;
  viewport_height = 94;

  width = viewport_width + side_bezels * 2;
  height = viewport_height + top_bezel + bottom_bezel;
  y_offset = (top_bezel - bottom_bezel) / 2;

  difference() {
    translate([ 0, y_offset, front_thickness - depth / 2 ])
        cube([ width, height, depth ], center = true);            // outline
    cube([ viewport_width, viewport_height, 30 ], center = true); // view area
    translate([ 0, y_offset, -depth / 2 ])
        cube([ width - wall_thickness * 2, height - wall_thickness * 2, depth ],
             center = true); // hole
  };

  // Wedges to hold the display
  translate([ -5, height / 2 + y_offset - wall_thickness, 0 ]) edge(5);
  translate([ 5, height / 2 + y_offset - wall_thickness, 0 ]) edge(5);
  translate([
    -width / 2 + wall_thickness + 2.5, height / 2 + y_offset - wall_thickness, 0
  ]) edge(5);
  translate([
    width / 2 - wall_thickness - 2.5, height / 2 + y_offset - wall_thickness, 0
  ]) edge(5);

  translate([ width / 4, -height / 2 + y_offset + wall_thickness + 2.5, 0 ])
      rotate([ 0, 180, 0 ]) bohrloch(5);
  translate([ -width / 4, -height / 2 + y_offset + wall_thickness + 2.5, 0 ])
      rotate([ 0, 180, 0 ]) bohrloch(5);

  // wedge for total hold
  translate([ 0, height / 2 + y_offset - wall_thickness, -depth + 4 ])
      edge(3, 18);
}

module bohrloch(height, hole = 1.5) {
  depth = 8;
  translate([ 0, 0, height / 2 ]) difference() {
    union() {
      cube([ 8, depth, height ], center = true);
      translate([ 4, depth / 2, 0 ]) rotate([ 0, 90, 90 ])
          edge(width = height, size = depth);
      translate([ -4 - depth, -depth / 2, 0 ]) rotate([ 0, 90, 180 ])
          edge(width = height, size = depth);
    }
    cylinder(h = height + 1, r = hole, center = true);
  }
}

module edge(size = 10, width = 5) {
  translate([ -width / 2, -size, -size ]) rotate([ 90, 0, 90 ])
      linear_extrude(width)
          polygon(points = [ [ 0, 0 ], [ size, 0 ], [ size, size ] ]);
}

module waveshare_7in5(straight = true) {
  color("grey") translate([ -85, -56, 0 ]) cube([ 170, 112, 1.5 ]);
  color("white") translate([ -79, -44, 0.01 ]) cube([ 158, 94, 1.5 ]);

  if (straight) {
    color("gold") translate([ -12, -70, 0 ]) cube([ 24, 14, 1 ]);
    color("gold") translate([ -7, -80, 0 ]) cube([ 14, 10, 1 ]);
  } else {
    color("gold") translate([ 12, -56, -3 ]) rotate([ 0, 90, 180 ])
        rotate_extrude(angle = 180) translate([ 3, 0, 0 ]) square([ 1, 24 ]);
    color("gold") translate([ -7, -56, -7 ]) cube([ 14, 10, 1 ]);
  }
}

module waveshare_esp32_driver(with_pinheader = true) {
  // board
  color("blue") cube([ 30, 49, 2 ]);
  // top side
  translate([ 6, 23, 2 ]) esp32();
  color("white") translate([ 24, 5, 2 ]) cube([ 5, 16, 2 ]);
  color("black") translate([ 1, 9, 2 ]) cube([ 4, 6, 2.5 ]);
  color("silver") translate([ 11, -1, 2 ]) cube([ 8, 6, 2.5 ]);
  translate([ 5, 0, 2 ]) button();
  translate([ 20, 0, 2 ]) button();
  // bottom side
  color("black") translate([ 8, 15.5, -3 ]) cube([ 4, 4, 3 ]);
  if (with_pinheader) {
    translate([ 3.5, 0, 0 ]) rotate([ 0, 180, 0 ]) smd_pinheader();
    translate([ 26, 0, 0 ]) rotate([ 0, 180, 0 ]) smd_pinheader();
  }
}

module smd_pinheader() {
  for (i = [0:18]) {
    translate([ 0, 1.27 + i * 2.54, 0 ]) rotate([ 0, 0, i * 180 ]) smd_pin();
  }
}

module smd_pin() {
  color("yellow") translate([ 0, 0, 2 ]) cube(2.54, center = true);
  color("gold") translate([ 0, 0, 5 ]) cube([ 0.7, 0.7, 10 ], center = true);
  color("gold") translate([ 1.5, 0, 0.35 ])
      cube([ 3, 0.7, 0.7 ], center = true);
}

module button() {
  color("silver") cube([ 4, 3, 1.5 ]);
  color("black") translate([ 2, 1.5, 1.5 ]) cylinder(1, 1, center = true);
}

module esp32() {
  color("black") cube([ 18, 26, 1 ]);
  color("silver") translate([ 1, 1, 1 ]) cube([ 16, 18, 3 ]);
}

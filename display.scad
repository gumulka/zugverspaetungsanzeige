module waveshare_7in5(straight = true) {
        color("grey") translate([-85, -56, 0]) cube([170, 112, 1.5]);
        color("white") translate([-79, -44, 0.01]) cube([158, 94, 1.5]);

        if (straight) {
                color("gold") translate([-12, -70, 0]) cube([24, 14, 1]);
                color("gold") translate([-7, -80, 0]) cube([14, 10, 1]);
        } else {
                color("gold") translate([12, -56, -3]) rotate([0, 90, 180])
                rotate_extrude(angle = 180) translate([3, 0, 0]) square([1, 24]);
                color("gold") translate([-7, -56, -7]) cube([14, 10, 1]);
        }
}

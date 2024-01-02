module waveshare_esp32_driver(with_pinheader = true) {
        // board
        color("blue") cube([30, 49, 2]);
        // top side
        translate([6, 23, 2]) esp32();
        color("white") translate([24, 5, 2]) cube([5, 16, 2]);
        color("black") translate([1, 9, 2]) cube([4, 6, 2.5]);
        color("silver") translate([11, -1, 2]) cube([8, 6, 2.5]);
        translate([5, 0, 2]) button();
        translate([20, 0, 2]) button();
        // bottom side
        color("black") translate([8, 15.5, -3]) cube([4, 4, 3]);
        if (with_pinheader) {
                translate([3.5, 0, 0]) rotate([0, 180, 0]) smd_pinheader();
                translate([26, 0, 0]) rotate([0, 180, 0]) smd_pinheader();
        }
}

module smd_pinheader() {
        for (i = [0: 18]) {
                translate([0, 1.27 + i * 2.54, 0]) rotate([0, 0, i * 180]) smd_pin();
        }
}

module smd_pin() {
        color("yellow") translate([0, 0, 2]) cube(2.54, center = true);
        color("gold") translate([0, 0, 5]) cube([0.7, 0.7, 10], center = true);
        color("gold") translate([1.5, 0, 0.35])
        cube([3, 0.7, 0.7], center = true);
}

module button() {
        color("silver") cube([4, 3, 1.5]);
        color("black") translate([2, 1.5, 1.5]) cylinder(1, 1, center = true);
}

module esp32() {
        color("black") cube([18, 26, 1]);
        color("silver") translate([1, 1, 1]) cube([16, 18, 3]);
}

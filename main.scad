include <esp32.scad>
include <gehause.scad>
include <display.scad>

$fn = 40;

frontside();

translate([0, -3, -1.5]) waveshare_7in5(false);

translate([13, -20, -5]) rotate([0, 180, 90]) waveshare_esp32_driver(false);

translate([0, 0, 1]) backplate();

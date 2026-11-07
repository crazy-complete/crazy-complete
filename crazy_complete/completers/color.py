# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for color names and color codes.'''

from .. import messages as m
from ..errors import CrazySchemaValidationError
from ..scheme_validator import check_non_empty_list, check_non_empty_string, check_type

CATEGORY = 'basic'

SYNOPSIS = r'''
['color']

['color', <TYPES>]
'''

SHORT = 'Complete color names and color codes'

LONG = r'''
`TYPES`:
  A list with one or more of the following:

  - `names`:  xterm color names
  - `xterm256`:  xterm 256-color codes (0-255)
  - `ansi_fg`: ANSI foreground color codes
  - `ansi_bg`: ANSI background color codes
  - `hex`:    hex color codes

  `ansi_fg` and `ansi_bg` may append the suffix `+bright`
  to also complete the bright colors.

  If `TYPES` is omitted, `names` is used.
'''

ALSO = {
    'choices': 'For completing from a custom set of values',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--color-names']
    complete: ['color']

  - option_strings: ['--color-xterm256']
    complete: ['color', ['xterm256']]

  - option_strings: ['--color-fg']
    complete: ['color', ['ansi_fg+bright']]

  - option_strings: ['--color-bg']
    complete: ['color', ['ansi_bg']]

  - option_strings: ['--color-hex']
    complete: ['color', ['hex']]
'''

OUTPUT = r'''
~ > example --color-names=<TAB>
Aqua   Fuchsia  Lime    Olive   Silver  Yellow
Black  Green    Maroon  Purple  Teal
Blue   Grey     Navy    Red     White

~ > example --color-xterm256=<TAB>
0     (Black (SYSTEM))  43              (Cyan3)  86       (Aquamarine1)
1    (Maroon (SYSTEM))  44      (DarkTurquoise)  87    (DarkSlateGray2)
[...]

~ > example --color-fg=<TAB>
30   (Black)  34     (Blue)  90   (Bright Black)  94     (Bright Blue)
31     (Red)  35  (Magenta)  91     (Bright Red)  95  (Bright Magenta)
32   (Green)  36     (Cyan)  92   (Bright Green)  96     (Bright Cyan)
33  (Yellow)  37    (White)  93  (Bright Yellow)  97    (Bright White)

~ > example --color-bg=<TAB>
40  (Black)  42   (Green)  44     (Blue)  46   (Cyan)
41    (Red)  43  (Yellow)  45  (Magenta)  47  (White)

~ > example --color-hex=<TAB>
#000000     (Black (SYSTEM))  #5f87d7       (SteelBlue3)
#0000af              (Blue3)  #5f87ff   (CornflowerBlue)
[...]
'''

_XTERM_NAMES = (
    'Black', 'Maroon', 'Green', 'Olive', 'Navy', 'Purple', 'Teal', 'Silver',
    'Grey', 'Red', 'Lime', 'Yellow', 'Blue', 'Fuchsia', 'Aqua', 'White',)

_ANSI_COLORS = (
    'Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White',)

_COLORS_256 = (
    ('0', 'Black (SYSTEM)'),
    ('1', 'Maroon (SYSTEM)'),
    ('2', 'Green (SYSTEM)'),
    ('3', 'Olive (SYSTEM)'),
    ('4', 'Navy (SYSTEM)'),
    ('5', 'Purple (SYSTEM)'),
    ('6', 'Teal (SYSTEM)'),
    ('7', 'Silver (SYSTEM)'),
    ('8', 'Grey (SYSTEM)'),
    ('9', 'Red (SYSTEM)'),
    ('10', 'Lime (SYSTEM)'),
    ('11', 'Yellow (SYSTEM)'),
    ('12', 'Blue (SYSTEM)'),
    ('13', 'Fuchsia (SYSTEM)'),
    ('14', 'Aqua (SYSTEM)'),
    ('15', 'White (SYSTEM)'),
    ('16', 'Grey0'),
    ('17', 'NavyBlue'),
    ('18', 'DarkBlue'),
    ('19', 'Blue3'),
    ('20', 'Blue3'),
    ('21', 'Blue1'),
    ('22', 'DarkGreen'),
    ('23', 'DeepSkyBlue4'),
    ('24', 'DeepSkyBlue4'),
    ('25', 'DeepSkyBlue4'),
    ('26', 'DodgerBlue3'),
    ('27', 'DodgerBlue2'),
    ('28', 'Green4'),
    ('29', 'SpringGreen4'),
    ('30', 'Turquoise4'),
    ('31', 'DeepSkyBlue3'),
    ('32', 'DeepSkyBlue3'),
    ('33', 'DodgerBlue1'),
    ('34', 'Green3'),
    ('35', 'SpringGreen3'),
    ('36', 'DarkCyan'),
    ('37', 'LightSeaGreen'),
    ('38', 'DeepSkyBlue2'),
    ('39', 'DeepSkyBlue1'),
    ('40', 'Green3'),
    ('41', 'SpringGreen3'),
    ('42', 'SpringGreen2'),
    ('43', 'Cyan3'),
    ('44', 'DarkTurquoise'),
    ('45', 'Turquoise2'),
    ('46', 'Green1'),
    ('47', 'SpringGreen2'),
    ('48', 'SpringGreen1'),
    ('49', 'MediumSpringGreen'),
    ('50', 'Cyan2'),
    ('51', 'Cyan1'),
    ('52', 'DarkRed'),
    ('53', 'DeepPink4'),
    ('54', 'Purple4'),
    ('55', 'Purple4'),
    ('56', 'Purple3'),
    ('57', 'BlueViolet'),
    ('58', 'Orange4'),
    ('59', 'Grey37'),
    ('60', 'MediumPurple4'),
    ('61', 'SlateBlue3'),
    ('62', 'SlateBlue3'),
    ('63', 'RoyalBlue1'),
    ('64', 'Chartreuse4'),
    ('65', 'DarkSeaGreen4'),
    ('66', 'PaleTurquoise4'),
    ('67', 'SteelBlue'),
    ('68', 'SteelBlue3'),
    ('69', 'CornflowerBlue'),
    ('70', 'Chartreuse3'),
    ('71', 'DarkSeaGreen4'),
    ('72', 'CadetBlue'),
    ('73', 'CadetBlue'),
    ('74', 'SkyBlue3'),
    ('75', 'SteelBlue1'),
    ('76', 'Chartreuse3'),
    ('77', 'PaleGreen3'),
    ('78', 'SeaGreen3'),
    ('79', 'Aquamarine3'),
    ('80', 'MediumTurquoise'),
    ('81', 'SteelBlue1'),
    ('82', 'Chartreuse2'),
    ('83', 'SeaGreen2'),
    ('84', 'SeaGreen1'),
    ('85', 'SeaGreen1'),
    ('86', 'Aquamarine1'),
    ('87', 'DarkSlateGray2'),
    ('88', 'DarkRed'),
    ('89', 'DeepPink4'),
    ('90', 'DarkMagenta'),
    ('91', 'DarkMagenta'),
    ('92', 'DarkViolet'),
    ('93', 'Purple'),
    ('94', 'Orange4'),
    ('95', 'LightPink4'),
    ('96', 'Plum4'),
    ('97', 'MediumPurple3'),
    ('98', 'MediumPurple3'),
    ('99', 'SlateBlue1'),
    ('100', 'Yellow4'),
    ('101', 'Wheat4'),
    ('102', 'Grey53'),
    ('103', 'LightSlateGrey'),
    ('104', 'MediumPurple'),
    ('105', 'LightSlateBlue'),
    ('106', 'Yellow4'),
    ('107', 'DarkOliveGreen3'),
    ('108', 'DarkSeaGreen'),
    ('109', 'LightSkyBlue3'),
    ('110', 'LightSkyBlue3'),
    ('111', 'SkyBlue2'),
    ('112', 'Chartreuse2'),
    ('113', 'DarkOliveGreen3'),
    ('114', 'PaleGreen3'),
    ('115', 'DarkSeaGreen3'),
    ('116', 'DarkSlateGray3'),
    ('117', 'SkyBlue1'),
    ('118', 'Chartreuse1'),
    ('119', 'LightGreen'),
    ('120', 'LightGreen'),
    ('121', 'PaleGreen1'),
    ('122', 'Aquamarine1'),
    ('123', 'DarkSlateGray1'),
    ('124', 'Red3'),
    ('125', 'DeepPink4'),
    ('126', 'MediumVioletRed'),
    ('127', 'Magenta3'),
    ('128', 'DarkViolet'),
    ('129', 'Purple'),
    ('130', 'DarkOrange3'),
    ('131', 'IndianRed'),
    ('132', 'HotPink3'),
    ('133', 'MediumOrchid3'),
    ('134', 'MediumOrchid'),
    ('135', 'MediumPurple2'),
    ('136', 'DarkGoldenrod'),
    ('137', 'LightSalmon3'),
    ('138', 'RosyBrown'),
    ('139', 'Grey63'),
    ('140', 'MediumPurple2'),
    ('141', 'MediumPurple1'),
    ('142', 'Gold3'),
    ('143', 'DarkKhaki'),
    ('144', 'NavajoWhite3'),
    ('145', 'Grey69'),
    ('146', 'LightSteelBlue3'),
    ('147', 'LightSteelBlue'),
    ('148', 'Yellow3'),
    ('149', 'DarkOliveGreen3'),
    ('150', 'DarkSeaGreen3'),
    ('151', 'DarkSeaGreen2'),
    ('152', 'LightCyan3'),
    ('153', 'LightSkyBlue1'),
    ('154', 'GreenYellow'),
    ('155', 'DarkOliveGreen2'),
    ('156', 'PaleGreen1'),
    ('157', 'DarkSeaGreen2'),
    ('158', 'DarkSeaGreen1'),
    ('159', 'PaleTurquoise1'),
    ('160', 'Red3'),
    ('161', 'DeepPink3'),
    ('162', 'DeepPink3'),
    ('163', 'Magenta3'),
    ('164', 'Magenta3'),
    ('165', 'Magenta2'),
    ('166', 'DarkOrange3'),
    ('167', 'IndianRed'),
    ('168', 'HotPink3'),
    ('169', 'HotPink2'),
    ('170', 'Orchid'),
    ('171', 'MediumOrchid1'),
    ('172', 'Orange3'),
    ('173', 'LightSalmon3'),
    ('174', 'LightPink3'),
    ('175', 'Pink3'),
    ('176', 'Plum3'),
    ('177', 'Violet'),
    ('178', 'Gold3'),
    ('179', 'LightGoldenrod3'),
    ('180', 'Tan'),
    ('181', 'MistyRose3'),
    ('182', 'Thistle3'),
    ('183', 'Plum2'),
    ('184', 'Yellow3'),
    ('185', 'Khaki3'),
    ('186', 'LightGoldenrod2'),
    ('187', 'LightYellow3'),
    ('188', 'Grey84'),
    ('189', 'LightSteelBlue1'),
    ('190', 'Yellow2'),
    ('191', 'DarkOliveGreen1'),
    ('192', 'DarkOliveGreen1'),
    ('193', 'DarkSeaGreen1'),
    ('194', 'Honeydew2'),
    ('195', 'LightCyan1'),
    ('196', 'Red1'),
    ('197', 'DeepPink2'),
    ('198', 'DeepPink1'),
    ('199', 'DeepPink1'),
    ('200', 'Magenta2'),
    ('201', 'Magenta1'),
    ('202', 'OrangeRed1'),
    ('203', 'IndianRed1'),
    ('204', 'IndianRed1'),
    ('205', 'HotPink'),
    ('206', 'HotPink'),
    ('207', 'MediumOrchid1'),
    ('208', 'DarkOrange'),
    ('209', 'Salmon1'),
    ('210', 'LightCoral'),
    ('211', 'PaleVioletRed1'),
    ('212', 'Orchid2'),
    ('213', 'Orchid1'),
    ('214', 'Orange1'),
    ('215', 'SandyBrown'),
    ('216', 'LightSalmon1'),
    ('217', 'LightPink1'),
    ('218', 'Pink1'),
    ('219', 'Plum1'),
    ('220', 'Gold1'),
    ('221', 'LightGoldenrod2'),
    ('222', 'LightGoldenrod2'),
    ('223', 'NavajoWhite1'),
    ('224', 'MistyRose1'),
    ('225', 'Thistle1'),
    ('226', 'Yellow1'),
    ('227', 'LightGoldenrod1'),
    ('228', 'Khaki1'),
    ('229', 'Wheat1'),
    ('230', 'Cornsilk1'),
    ('231', 'Grey100'),
    ('232', 'Grey3'),
    ('233', 'Grey7'),
    ('234', 'Grey11'),
    ('235', 'Grey15'),
    ('236', 'Grey19'),
    ('237', 'Grey23'),
    ('238', 'Grey27'),
    ('239', 'Grey30'),
    ('240', 'Grey35'),
    ('241', 'Grey39'),
    ('242', 'Grey42'),
    ('243', 'Grey46'),
    ('244', 'Grey50'),
    ('245', 'Grey54'),
    ('246', 'Grey58'),
    ('247', 'Grey62'),
    ('248', 'Grey66'),
    ('249', 'Grey70'),
    ('250', 'Grey74'),
    ('251', 'Grey78'),
    ('252', 'Grey82'),
    ('253', 'Grey85'),
    ('254', 'Grey89'),
    ('255', 'Grey93'),
)

_COLORS_HEX = (
    ('#000000', 'Black (SYSTEM)'),
    ('#800000', 'Maroon (SYSTEM)'),
    ('#008000', 'Green (SYSTEM)'),
    ('#808000', 'Olive (SYSTEM)'),
    ('#000080', 'Navy (SYSTEM)'),
    ('#800080', 'Purple (SYSTEM)'),
    ('#008080', 'Teal (SYSTEM)'),
    ('#c0c0c0', 'Silver (SYSTEM)'),
    ('#808080', 'Grey (SYSTEM)'),
    ('#ff0000', 'Red (SYSTEM)'),
    ('#00ff00', 'Lime (SYSTEM)'),
    ('#ffff00', 'Yellow (SYSTEM)'),
    ('#0000ff', 'Blue (SYSTEM)'),
    ('#ff00ff', 'Fuchsia (SYSTEM)'),
    ('#00ffff', 'Aqua (SYSTEM)'),
    ('#ffffff', 'White (SYSTEM)'),
    ('#00005f', 'NavyBlue'),
    ('#000087', 'DarkBlue'),
    ('#0000af', 'Blue3'),
    ('#0000d7', 'Blue3'),
    ('#005f00', 'DarkGreen'),
    ('#005f5f', 'DeepSkyBlue4'),
    ('#005f87', 'DeepSkyBlue4'),
    ('#005faf', 'DeepSkyBlue4'),
    ('#005fd7', 'DodgerBlue3'),
    ('#005fff', 'DodgerBlue2'),
    ('#008700', 'Green4'),
    ('#00875f', 'SpringGreen4'),
    ('#008787', 'Turquoise4'),
    ('#0087af', 'DeepSkyBlue3'),
    ('#0087d7', 'DeepSkyBlue3'),
    ('#0087ff', 'DodgerBlue1'),
    ('#00af00', 'Green3'),
    ('#00af5f', 'SpringGreen3'),
    ('#00af87', 'DarkCyan'),
    ('#00afaf', 'LightSeaGreen'),
    ('#00afd7', 'DeepSkyBlue2'),
    ('#00afff', 'DeepSkyBlue1'),
    ('#00d700', 'Green3'),
    ('#00d75f', 'SpringGreen3'),
    ('#00d787', 'SpringGreen2'),
    ('#00d7af', 'Cyan3'),
    ('#00d7d7', 'DarkTurquoise'),
    ('#00d7ff', 'Turquoise2'),
    ('#00ff5f', 'SpringGreen2'),
    ('#00ff87', 'SpringGreen1'),
    ('#00ffaf', 'MediumSpringGreen'),
    ('#00ffd7', 'Cyan2'),
    ('#5f0000', 'DarkRed'),
    ('#5f005f', 'DeepPink4'),
    ('#5f0087', 'Purple4'),
    ('#5f00af', 'Purple4'),
    ('#5f00d7', 'Purple3'),
    ('#5f00ff', 'BlueViolet'),
    ('#5f5f00', 'Orange4'),
    ('#5f5f5f', 'Grey37'),
    ('#5f5f87', 'MediumPurple4'),
    ('#5f5faf', 'SlateBlue3'),
    ('#5f5fd7', 'SlateBlue3'),
    ('#5f5fff', 'RoyalBlue1'),
    ('#5f8700', 'Chartreuse4'),
    ('#5f875f', 'DarkSeaGreen4'),
    ('#5f8787', 'PaleTurquoise4'),
    ('#5f87af', 'SteelBlue'),
    ('#5f87d7', 'SteelBlue3'),
    ('#5f87ff', 'CornflowerBlue'),
    ('#5faf00', 'Chartreuse3'),
    ('#5faf5f', 'DarkSeaGreen4'),
    ('#5faf87', 'CadetBlue'),
    ('#5fafaf', 'CadetBlue'),
    ('#5fafd7', 'SkyBlue3'),
    ('#5fafff', 'SteelBlue1'),
    ('#5fd700', 'Chartreuse3'),
    ('#5fd75f', 'PaleGreen3'),
    ('#5fd787', 'SeaGreen3'),
    ('#5fd7af', 'Aquamarine3'),
    ('#5fd7d7', 'MediumTurquoise'),
    ('#5fd7ff', 'SteelBlue1'),
    ('#5fff00', 'Chartreuse2'),
    ('#5fff5f', 'SeaGreen2'),
    ('#5fff87', 'SeaGreen1'),
    ('#5fffaf', 'SeaGreen1'),
    ('#5fffd7', 'Aquamarine1'),
    ('#5fffff', 'DarkSlateGray2'),
    ('#870000', 'DarkRed'),
    ('#87005f', 'DeepPink4'),
    ('#870087', 'DarkMagenta'),
    ('#8700af', 'DarkMagenta'),
    ('#8700d7', 'DarkViolet'),
    ('#8700ff', 'Purple'),
    ('#875f00', 'Orange4'),
    ('#875f5f', 'LightPink4'),
    ('#875f87', 'Plum4'),
    ('#875faf', 'MediumPurple3'),
    ('#875fd7', 'MediumPurple3'),
    ('#875fff', 'SlateBlue1'),
    ('#878700', 'Yellow4'),
    ('#87875f', 'Wheat4'),
    ('#878787', 'Grey53'),
    ('#8787af', 'LightSlateGrey'),
    ('#8787d7', 'MediumPurple'),
    ('#8787ff', 'LightSlateBlue'),
    ('#87af00', 'Yellow4'),
    ('#87af5f', 'DarkOliveGreen3'),
    ('#87af87', 'DarkSeaGreen'),
    ('#87afaf', 'LightSkyBlue3'),
    ('#87afd7', 'LightSkyBlue3'),
    ('#87afff', 'SkyBlue2'),
    ('#87d700', 'Chartreuse2'),
    ('#87d75f', 'DarkOliveGreen3'),
    ('#87d787', 'PaleGreen3'),
    ('#87d7af', 'DarkSeaGreen3'),
    ('#87d7d7', 'DarkSlateGray3'),
    ('#87d7ff', 'SkyBlue1'),
    ('#87ff00', 'Chartreuse1'),
    ('#87ff5f', 'LightGreen'),
    ('#87ff87', 'LightGreen'),
    ('#87ffaf', 'PaleGreen1'),
    ('#87ffd7', 'Aquamarine1'),
    ('#87ffff', 'DarkSlateGray1'),
    ('#af0000', 'Red3'),
    ('#af005f', 'DeepPink4'),
    ('#af0087', 'MediumVioletRed'),
    ('#af00af', 'Magenta3'),
    ('#af00d7', 'DarkViolet'),
    ('#af00ff', 'Purple'),
    ('#af5f00', 'DarkOrange3'),
    ('#af5f5f', 'IndianRed'),
    ('#af5f87', 'HotPink3'),
    ('#af5faf', 'MediumOrchid3'),
    ('#af5fd7', 'MediumOrchid'),
    ('#af5fff', 'MediumPurple2'),
    ('#af8700', 'DarkGoldenrod'),
    ('#af875f', 'LightSalmon3'),
    ('#af8787', 'RosyBrown'),
    ('#af87af', 'Grey63'),
    ('#af87d7', 'MediumPurple2'),
    ('#af87ff', 'MediumPurple1'),
    ('#afaf00', 'Gold3'),
    ('#afaf5f', 'DarkKhaki'),
    ('#afaf87', 'NavajoWhite3'),
    ('#afafaf', 'Grey69'),
    ('#afafd7', 'LightSteelBlue3'),
    ('#afafff', 'LightSteelBlue'),
    ('#afd700', 'Yellow3'),
    ('#afd75f', 'DarkOliveGreen3'),
    ('#afd787', 'DarkSeaGreen3'),
    ('#afd7af', 'DarkSeaGreen2'),
    ('#afd7d7', 'LightCyan3'),
    ('#afd7ff', 'LightSkyBlue1'),
    ('#afff00', 'GreenYellow'),
    ('#afff5f', 'DarkOliveGreen2'),
    ('#afff87', 'PaleGreen1'),
    ('#afffaf', 'DarkSeaGreen2'),
    ('#afffd7', 'DarkSeaGreen1'),
    ('#afffff', 'PaleTurquoise1'),
    ('#d70000', 'Red3'),
    ('#d7005f', 'DeepPink3'),
    ('#d70087', 'DeepPink3'),
    ('#d700af', 'Magenta3'),
    ('#d700d7', 'Magenta3'),
    ('#d700ff', 'Magenta2'),
    ('#d75f00', 'DarkOrange3'),
    ('#d75f5f', 'IndianRed'),
    ('#d75f87', 'HotPink3'),
    ('#d75faf', 'HotPink2'),
    ('#d75fd7', 'Orchid'),
    ('#d75fff', 'MediumOrchid1'),
    ('#d78700', 'Orange3'),
    ('#d7875f', 'LightSalmon3'),
    ('#d78787', 'LightPink3'),
    ('#d787af', 'Pink3'),
    ('#d787d7', 'Plum3'),
    ('#d787ff', 'Violet'),
    ('#d7af00', 'Gold3'),
    ('#d7af5f', 'LightGoldenrod3'),
    ('#d7af87', 'Tan'),
    ('#d7afaf', 'MistyRose3'),
    ('#d7afd7', 'Thistle3'),
    ('#d7afff', 'Plum2'),
    ('#d7d700', 'Yellow3'),
    ('#d7d75f', 'Khaki3'),
    ('#d7d787', 'LightGoldenrod2'),
    ('#d7d7af', 'LightYellow3'),
    ('#d7d7d7', 'Grey84'),
    ('#d7d7ff', 'LightSteelBlue1'),
    ('#d7ff00', 'Yellow2'),
    ('#d7ff5f', 'DarkOliveGreen1'),
    ('#d7ff87', 'DarkOliveGreen1'),
    ('#d7ffaf', 'DarkSeaGreen1'),
    ('#d7ffd7', 'Honeydew2'),
    ('#d7ffff', 'LightCyan1'),
    ('#ff005f', 'DeepPink2'),
    ('#ff0087', 'DeepPink1'),
    ('#ff00af', 'DeepPink1'),
    ('#ff00d7', 'Magenta2'),
    ('#ff5f00', 'OrangeRed1'),
    ('#ff5f5f', 'IndianRed1'),
    ('#ff5f87', 'IndianRed1'),
    ('#ff5faf', 'HotPink'),
    ('#ff5fd7', 'HotPink'),
    ('#ff5fff', 'MediumOrchid1'),
    ('#ff8700', 'DarkOrange'),
    ('#ff875f', 'Salmon1'),
    ('#ff8787', 'LightCoral'),
    ('#ff87af', 'PaleVioletRed1'),
    ('#ff87d7', 'Orchid2'),
    ('#ff87ff', 'Orchid1'),
    ('#ffaf00', 'Orange1'),
    ('#ffaf5f', 'SandyBrown'),
    ('#ffaf87', 'LightSalmon1'),
    ('#ffafaf', 'LightPink1'),
    ('#ffafd7', 'Pink1'),
    ('#ffafff', 'Plum1'),
    ('#ffd700', 'Gold1'),
    ('#ffd75f', 'LightGoldenrod2'),
    ('#ffd787', 'LightGoldenrod2'),
    ('#ffd7af', 'NavajoWhite1'),
    ('#ffd7d7', 'MistyRose1'),
    ('#ffd7ff', 'Thistle1'),
    ('#ffff5f', 'LightGoldenrod1'),
    ('#ffff87', 'Khaki1'),
    ('#ffffaf', 'Wheat1'),
    ('#ffffd7', 'Cornsilk1'),
    ('#080808', 'Grey3'),
    ('#121212', 'Grey7'),
    ('#1c1c1c', 'Grey11'),
    ('#262626', 'Grey15'),
    ('#303030', 'Grey19'),
    ('#3a3a3a', 'Grey23'),
    ('#444444', 'Grey27'),
    ('#4e4e4e', 'Grey30'),
    ('#585858', 'Grey35'),
    ('#626262', 'Grey39'),
    ('#6c6c6c', 'Grey42'),
    ('#767676', 'Grey46'),
    ('#8a8a8a', 'Grey54'),
    ('#949494', 'Grey58'),
    ('#9e9e9e', 'Grey62'),
    ('#a8a8a8', 'Grey66'),
    ('#b2b2b2', 'Grey70'),
    ('#bcbcbc', 'Grey74'),
    ('#c6c6c6', 'Grey78'),
    ('#d0d0d0', 'Grey82'),
    ('#dadada', 'Grey85'),
    ('#e4e4e4', 'Grey89'),
    ('#eeeeee', 'Grey93'),
)



def _ansi_set(foreground, bright):
    '''Build the ANSI color (value, description) pairs.'''
    first = '3' if foreground else '4'
    bright_first = '9' if foreground else '10'

    pairs = [(first + str(i), name) for i, name in enumerate(_ANSI_COLORS)]

    if bright:
        pairs += [
            (bright_first + str(i), 'Bright ' + name)
            for i, name in enumerate(_ANSI_COLORS)]

    return pairs


_COLOR_SETS = {
    'names': [(name, None) for name in _XTERM_NAMES],
    'xterm256': _COLORS_256,
    'ansi_fg': _ansi_set(True, False),
    'ansi_fg+bright': _ansi_set(True, True),
    'ansi_bg': _ansi_set(False, False),
    'ansi_bg+bright': _ansi_set(False, True),
    'hex': _COLORS_HEX,
}

_ALLOWED_TYPES = tuple(_COLOR_SETS)

_DEFAULT_TYPES = ['names']

_error = CrazySchemaValidationError


def validate(_ctxt, arguments):
    '''Validate YAML for color completer'''
    types = arguments.get_optional_arg(_DEFAULT_TYPES)
    arguments.require_no_more()

    check_type(types, (list,), 'types')
    check_non_empty_list(types, 'types')

    # The default value is a plain list without trace information,
    # its items are known to be valid.
    if types.value is _DEFAULT_TYPES:
        return

    for i, item in enumerate(types.value):
        name = 'types[%s]' % i
        check_type(item, (str,), name)
        check_non_empty_string(item, name)

        if item.value not in _ALLOWED_TYPES:
            values = ', '.join(_ALLOWED_TYPES)
            msg = '%s: %s' % (name, m.invalid_value_expected_values(values))
            raise _error(msg, item)


def _collect(types):
    '''Collect (value, description) pairs for the given types.'''
    pairs = []
    for type_ in types:
        for pair in _COLOR_SETS[type_]:
            if pair[0] not in [p[0] for p in pairs]:
                pairs.append(pair)
    return pairs


def _choices(pairs):
    '''Return a list of values or a value/description dictionary.'''
    if all(desc is None for _, desc in pairs):
        return [value for value, _ in pairs]

    return {value: desc for value, desc in pairs}


def bash(completer, ctxt, trace, types=('names',)):
    '''Implement color for bash'''
    return completer.complete_from_def(ctxt, trace, ['choices', _choices(_collect(types))])


def fish(completer, ctxt, trace, types=('names',)):
    '''Implement color for fish'''
    return completer.complete_from_def(ctxt, trace, ['choices', _choices(_collect(types))])


def zsh(completer, ctxt, trace, types=('names',)):
    '''Implement color for zsh'''
    return completer.complete_from_def(ctxt, trace, ['choices', _choices(_collect(types))])

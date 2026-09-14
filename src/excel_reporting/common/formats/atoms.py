from .colors import (
    gw_blue,
    gw_light_blue,
    gw_blue_green,
    gw_green,
    gw_orange,
    gw_red,
    row_blue,
    row_light_blue,
    row_orange,
    row_green,
    row_gray,
    row_light_gray,
    row_dark_gray,
)

locked = {"locked": True}
hidden = {"hidden": True}

# region Background
bg_white = {"bg_color": "white"}
bg_red = {"bg_color": gw_red}
bg_green = {"bg_color": gw_green}
bg_orange = {"bg_color": gw_orange}
bg_blue = {"bg_color": gw_blue}
bg_light_blue = {"bg_color": gw_light_blue}
bg_blue_green = {"bg_color": gw_blue_green}
bg_row_blue = {"bg_color": row_blue}
bg_row_light_blue = {"bg_color": row_light_blue}
bg_row_orange = {"bg_color": row_orange}
bg_row_green = {"bg_color": row_green}
bg_row_gray = {"bg_color": row_gray}
bg_row_light_gray = {"bg_color": row_light_gray}
bg_row_dark_gray = {"bg_color": row_dark_gray}
# endregion Background

# region Alignment
align_left = {"align": "left"}
align_center = {"align": "center"}
align_right = {"align": "right"}
v_top = {"valign": "vtop"}
v_center = {"valign": "vcenter"}
v_bottom = {"valign": "vbottom"}
# endregion Alignment

# region Border
bt = {"top": 1}
br = {"right": 1}
bb = {"bottom": 1}
bl = {"left": 1}
b_all = {"border": 1}
b_diag = {"diag_border": 1}

bt_bold = {"top": 2}
br_bold = {"right": 2}
bb_bold = {"bottom": 2}
bl_bold = {"left": 2}
b_all_bold = {"border": 2}
b_diag_bold = {"diag_border": 2}

bt_xbold = {"top": 5}
br_xbold = {"right": 5}
bb_xbold = {"bottom": 5}
bl_xbold = {"left": 5}
b_all_xbold = {"border": 5}
b_diag_xbold = {"diag_border": 5}

bt_double = {"top": 6}
br_double = {"right": 6}
bb_double = {"bottom": 6}
bl_double = {"left": 6}
b_all_double = {"border": 6}
b_diag_double = {"diag_border": 6}

bt_dot = {"top": 7}
br_dot = {"right": 7}
bb_dot = {"bottom": 7}
bl_dot = {"left": 7}
b_all_dot = {"border": 7}
b_diag_dot = {"diag_border": 7}

bt_dash = {"top": 3}
br_dash = {"right": 3}
bb_dash = {"bottom": 3}
bl_dash = {"left": 3}
b_all_dash = {"border": 3}
b_diag_dash = {"diag_border": 3}

bt_dash_sparse = {"top": 4}
br_dash_sparse = {"right": 4}
bb_dash_sparse = {"bottom": 4}
bl_dash_sparse = {"left": 4}
b_all_dash_sparse = {"border": 4}
b_diag_dash_sparse = {"diag_border": 4}

bt_d_dash = {"top": 9}
br_d_dash = {"right": 9}
bb_d_dash = {"bottom": 9}
bl_d_dash = {"left": 9}
b_all_d_dash = {"border": 9}
b_diag_d_dash = {"diag_border": 9}

bt_dd_dash = {"top": 11}
br_dd_dash = {"right": 11}
bb_dd_dash = {"bottom": 11}
bl_dd_dash = {"left": 11}
b_all_dd_dash = {"border": 11}
b_diag_dd_dash = {"diag_border": 11}

b_bl_tr = {"diag_type": 1}
b_tl_br = {"diag_type": 2}
b_cross = {"diag_type": 3}

bt_red = {"top_color": gw_red}
br_red = {"right_color": gw_red}
bb_red = {"bottom_color": gw_red}
bl_red = {"left_color": gw_red}
b_all_red = {"border_color": gw_red}
b_diag_red = {"diag_color": gw_red}
# endregion Border

# region Font
ft_11 = {"font_size": 11}
ft_12 = {"font_size": 12}
ft_14 = {"font_size": 14}
ft_16 = {"font_size": 16}
ft_18 = {"font_size": 18}
ft_20 = {"font_size": 20}
ft_24 = {"font_size": 24}
ft_28 = {"font_size": 28}

ft_white = {"font_color": "white"}
ft_red = {"font_color": gw_red}

bold = {"bold": True}
italic = {"italic": True}
strikeout = {"font_strikeout": True}
underline = {"underline": 1}
underline_double = {"underline": 2}
acct_underline = {"underline": 33}
acct_underline_double = {"underline": 34}
superscript = {"font_script": 1}
subscript = {"font_script": 2}

text_wrap = {"text_wrap": True}
shrink_to_fit = {"shrink": True}

indent_1 = {"indent": 1}
indent_2 = {"indent": 2}
indent_4 = {"indent": 4}
indent_8 = {"indent": 8}
# endregion Font

# region Number Format
fmt_int = {"num_format": "0"}
fmt_decimal = {"num_format": "0.00"}
fmt_int_comma = {"num_format": "#,##0"}
fmt_decimal_comma = {"num_format": "#,##0.00"}
fmt_percent = {"num_format": "0.00%"}
fmt_percent_int = {"num_format": "0%"}
fmt_currency = {"num_format": "$#,##0.00"}
fmt_currency_int = {"num_format": "$#,##0"}
fmt_acct = {"num_format": "$#,##0.00_);($#,##0.00)"}
fmt_int_comma_cond = {"num_format": "#,##0;[Red]-#,##0"}
fmt_decimal_comma_cond = {"num_format": "#,##0.00;[Red]-#,##0.00"}
fmt_acct_cond = {"num_format": "$#,##0.00_);[Red]($#,##0.00)"}

fmt_iso_date = {"num_format": "yyyy-mm-dd"}
fmt_iso_datetime = {"num_format": "yyyy-mm-dd hh:mm"}
fmt_date = {"num_format": "mm/dd/yyyy"}
fmt_datetime = {"num_format": "mm/dd/yyyy hh:mm"}
fmt_time = {"num_format": "hh:mm"}
fmt_month_name = {"num_format": "d mmmm yyyy"}
fmt_month_name_short = {"num_format": "d mmm yyyy"}
fmt_day_name = {"num_format": "dddd, mmmm d, yyyy"}
fmt_day_name_short = {"num_format": "ddd, mmm d, yyyy"}
# endregion Number Format

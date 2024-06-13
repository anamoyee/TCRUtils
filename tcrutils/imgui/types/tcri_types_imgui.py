# type: ignore
try:

  class ImguiType:
    ALWAYS: int
    APPEARING: int
    BACKEND_HAS_GAMEPAD: int
    BACKEND_HAS_MOUSE_CURSORS: int
    BACKEND_HAS_SET_MOUSE_POS: int
    BACKEND_NONE: int
    BACKEND_RENDERER_HAS_VTX_OFFSET: int
    BUTTON_MOUSE_BUTTON_LEFT: int
    BUTTON_MOUSE_BUTTON_MIDDLE: int
    BUTTON_MOUSE_BUTTON_RIGHT: int
    BUTTON_NONE: int
    COLOR_BORDER: int
    COLOR_BORDER_SHADOW: int
    COLOR_BUTTON: int
    COLOR_BUTTON_ACTIVE: int
    COLOR_BUTTON_HOVERED: int
    COLOR_CHECK_MARK: int
    COLOR_CHILD_BACKGROUND: int
    COLOR_COUNT: int
    COLOR_DRAG_DROP_TARGET: int
    COLOR_EDIT_ALPHA_BAR: int
    COLOR_EDIT_ALPHA_PREVIEW: int
    COLOR_EDIT_ALPHA_PREVIEW_HALF: int
    COLOR_EDIT_DEFAULT_OPTIONS: int
    COLOR_EDIT_DISPLAY_HEX: int
    COLOR_EDIT_DISPLAY_HSV: int
    COLOR_EDIT_DISPLAY_RGB: int
    COLOR_EDIT_FLOAT: int
    COLOR_EDIT_HDR: int
    COLOR_EDIT_INPUT_HSV: int
    COLOR_EDIT_INPUT_RGB: int
    COLOR_EDIT_NONE: int
    COLOR_EDIT_NO_ALPHA: int
    COLOR_EDIT_NO_BORDER: int
    COLOR_EDIT_NO_DRAG_DROP: int
    COLOR_EDIT_NO_INPUTS: int
    COLOR_EDIT_NO_LABEL: int
    COLOR_EDIT_NO_OPTIONS: int
    COLOR_EDIT_NO_PICKER: int
    COLOR_EDIT_NO_SIDE_PREVIEW: int
    COLOR_EDIT_NO_SMALL_PREVIEW: int
    COLOR_EDIT_NO_TOOLTIP: int
    COLOR_EDIT_PICKER_HUE_BAR: int
    COLOR_EDIT_PICKER_HUE_WHEEL: int
    COLOR_EDIT_UINT8: int
    COLOR_FRAME_BACKGROUND: int
    COLOR_FRAME_BACKGROUND_ACTIVE: int
    COLOR_FRAME_BACKGROUND_HOVERED: int
    COLOR_HEADER: int
    COLOR_HEADER_ACTIVE: int
    COLOR_HEADER_HOVERED: int
    COLOR_MENUBAR_BACKGROUND: int
    COLOR_MODAL_WINDOW_DIM_BACKGROUND: int
    COLOR_NAV_HIGHLIGHT: int
    COLOR_NAV_WINDOWING_DIM_BACKGROUND: int
    COLOR_NAV_WINDOWING_HIGHLIGHT: int
    COLOR_PLOT_HISTOGRAM: int
    COLOR_PLOT_HISTOGRAM_HOVERED: int
    COLOR_PLOT_LINES: int
    COLOR_PLOT_LINES_HOVERED: int
    COLOR_POPUP_BACKGROUND: int
    COLOR_RESIZE_GRIP: int
    COLOR_RESIZE_GRIP_ACTIVE: int
    COLOR_RESIZE_GRIP_HOVERED: int
    COLOR_SCROLLBAR_BACKGROUND: int
    COLOR_SCROLLBAR_GRAB: int
    COLOR_SCROLLBAR_GRAB_ACTIVE: int
    COLOR_SCROLLBAR_GRAB_HOVERED: int
    COLOR_SEPARATOR: int
    COLOR_SEPARATOR_ACTIVE: int
    COLOR_SEPARATOR_HOVERED: int
    COLOR_SLIDER_GRAB: int
    COLOR_SLIDER_GRAB_ACTIVE: int
    COLOR_TAB: int
    COLOR_TABLE_BORDER_LIGHT: int
    COLOR_TABLE_BORDER_STRONG: int
    COLOR_TABLE_HEADER_BACKGROUND: int
    COLOR_TABLE_ROW_BACKGROUND: int
    COLOR_TABLE_ROW_BACKGROUND_ALT: int
    COLOR_TAB_ACTIVE: int
    COLOR_TAB_HOVERED: int
    COLOR_TAB_UNFOCUSED: int
    COLOR_TAB_UNFOCUSED_ACTIVE: int
    COLOR_TEXT: int
    COLOR_TEXT_DISABLED: int
    COLOR_TEXT_SELECTED_BACKGROUND: int
    COLOR_TITLE_BACKGROUND: int
    COLOR_TITLE_BACKGROUND_ACTIVE: int
    COLOR_TITLE_BACKGROUND_COLLAPSED: int
    COLOR_WINDOW_BACKGROUND: int
    COMBO_HEIGHT_LARGE: int
    COMBO_HEIGHT_LARGEST: int
    COMBO_HEIGHT_MASK: int
    COMBO_HEIGHT_REGULAR: int
    COMBO_HEIGHT_SMALL: int
    COMBO_NONE: int
    COMBO_NO_ARROW_BUTTON: int
    COMBO_NO_PREVIEW: int
    COMBO_POPUP_ALIGN_LEFT: int
    CONFIG_IS_RGB: int
    CONFIG_IS_TOUCH_SCREEN: int
    CONFIG_NAV_ENABLE_GAMEPAD: int
    CONFIG_NAV_ENABLE_KEYBOARD: int
    CONFIG_NAV_ENABLE_SET_MOUSE_POS: int
    CONFIG_NAV_NO_CAPTURE_KEYBOARD: int
    CONFIG_NONE: int
    CONFIG_NO_MOUSE: int
    CONFIG_NO_MOUSE_CURSOR_CHANGE: int
    DATA_TYPE_DOUBLE: int
    DATA_TYPE_FLOAT: int
    DATA_TYPE_S16: int
    DATA_TYPE_S32: int
    DATA_TYPE_S64: int
    DATA_TYPE_S8: int
    DATA_TYPE_U16: int
    DATA_TYPE_U32: int
    DATA_TYPE_U64: int
    DATA_TYPE_U8: int
    DIRECTION_DOWN: int
    DIRECTION_LEFT: int
    DIRECTION_NONE: int
    DIRECTION_RIGHT: int
    DIRECTION_UP: int
    DRAG_DROP_ACCEPT_BEFORE_DELIVERY: int
    DRAG_DROP_ACCEPT_NO_DRAW_DEFAULT_RECT: int
    DRAG_DROP_ACCEPT_NO_PREVIEW_TOOLTIP: int
    DRAG_DROP_ACCEPT_PEEK_ONLY: int
    DRAG_DROP_NONE: int
    DRAG_DROP_SOURCE_ALLOW_NULL_ID: int
    DRAG_DROP_SOURCE_AUTO_EXPIRE_PAYLOAD: int
    DRAG_DROP_SOURCE_EXTERN: int
    DRAG_DROP_SOURCE_NO_DISABLE_HOVER: int
    DRAG_DROP_SOURCE_NO_HOLD_TO_OPEN_OTHERS: int
    DRAG_DROP_SOURCE_NO_PREVIEW_TOOLTIP: int
    DRAW_CLOSED: int
    DRAW_CORNER_ALL: int
    DRAW_CORNER_BOTTOM: int
    DRAW_CORNER_BOTTOM_LEFT: int
    DRAW_CORNER_BOTTOM_RIGHT: int
    DRAW_CORNER_LEFT: int
    DRAW_CORNER_NONE: int
    DRAW_CORNER_RIGHT: int
    DRAW_CORNER_TOP: int
    DRAW_CORNER_TOP_LEFT: int
    DRAW_CORNER_TOP_RIGHT: int
    DRAW_LIST_ALLOW_VTX_OFFSET: int
    DRAW_LIST_ANTI_ALIASED_FILL: int
    DRAW_LIST_ANTI_ALIASED_LINES: int
    DRAW_LIST_ANTI_ALIASED_LINES_USE_TEX: int
    DRAW_LIST_NONE: int
    DRAW_NONE: int
    DRAW_ROUND_CORNERS_ALL: int
    DRAW_ROUND_CORNERS_BOTTOM: int
    DRAW_ROUND_CORNERS_BOTTOM_LEFT: int
    DRAW_ROUND_CORNERS_BOTTOM_RIGHT: int
    DRAW_ROUND_CORNERS_LEFT: int
    DRAW_ROUND_CORNERS_NONE: int
    DRAW_ROUND_CORNERS_RIGHT: int
    DRAW_ROUND_CORNERS_TOP: int
    DRAW_ROUND_CORNERS_TOP_LEFT: int
    DRAW_ROUND_CORNERS_TOP_RIGHT: int
    FIRST_USE_EVER: int
    FLOAT_MAX: float
    FLOAT_MIN: float
    FOCUS_ANY_WINDOW: int
    FOCUS_CHILD_WINDOWS: int
    FOCUS_NONE: int
    FOCUS_ROOT_AND_CHILD_WINDOWS: int
    FOCUS_ROOT_WINDOW: int
    FONT_ATLAS_NONE: int
    FONT_ATLAS_NO_BAKED_LINES: int
    FONT_ATLAS_NO_MOUSE_CURSOR: int
    FONT_ATLAS_NO_POWER_OF_TWO_HEIGHT: int
    HOVERED_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM: int
    HOVERED_ALLOW_WHEN_BLOCKED_BY_POPUP: int
    HOVERED_ALLOW_WHEN_DISABLED: int
    HOVERED_ALLOW_WHEN_OVERLAPPED: int
    HOVERED_ANY_WINDOW: int
    HOVERED_CHILD_WINDOWS: int
    HOVERED_NONE: int
    HOVERED_RECT_ONLY: int
    HOVERED_ROOT_AND_CHILD_WINDOWS: int
    HOVERED_ROOT_WINDOW: int
    INDEX_SIZE: int
    INPUT_TEXT_ALLOW_TAB_INPUT: int
    INPUT_TEXT_ALWAYS_INSERT_MODE: int
    INPUT_TEXT_ALWAYS_OVERWRITE: int
    INPUT_TEXT_AUTO_SELECT_ALL: int
    INPUT_TEXT_CALLBACK_ALWAYS: int
    INPUT_TEXT_CALLBACK_CHAR_FILTER: int
    INPUT_TEXT_CALLBACK_COMPLETION: int
    INPUT_TEXT_CALLBACK_EDIT: int
    INPUT_TEXT_CALLBACK_HISTORY: int
    INPUT_TEXT_CALLBACK_RESIZE: int
    INPUT_TEXT_CHARS_DECIMAL: int
    INPUT_TEXT_CHARS_HEXADECIMAL: int
    INPUT_TEXT_CHARS_NO_BLANK: int
    INPUT_TEXT_CHARS_SCIENTIFIC: int
    INPUT_TEXT_CHARS_UPPERCASE: int
    INPUT_TEXT_CTRL_ENTER_FOR_NEW_LINE: int
    INPUT_TEXT_ENTER_RETURNS_TRUE: int
    INPUT_TEXT_NONE: int
    INPUT_TEXT_NO_HORIZONTAL_SCROLL: int
    INPUT_TEXT_NO_UNDO_REDO: int
    INPUT_TEXT_PASSWORD: int
    INPUT_TEXT_READ_ONLY: int
    KEY_A: int
    KEY_BACKSPACE: int
    KEY_C: int
    KEY_DELETE: int
    KEY_DOWN_ARROW: int
    KEY_END: int
    KEY_ENTER: int
    KEY_ESCAPE: int
    KEY_HOME: int
    KEY_INSERT: int
    KEY_LEFT_ARROW: int
    KEY_MOD_ALT: int
    KEY_MOD_CTRL: int
    KEY_MOD_NONE: int
    KEY_MOD_SHIFT: int
    KEY_MOD_SUPER: int
    KEY_PAD_ENTER: int
    KEY_PAGE_DOWN: int
    KEY_PAGE_UP: int
    KEY_RIGHT_ARROW: int
    KEY_SPACE: int
    KEY_TAB: int
    KEY_UP_ARROW: int
    KEY_V: int
    KEY_X: int
    KEY_Y: int
    KEY_Z: int
    MOUSE_BUTTON_LEFT: int
    MOUSE_BUTTON_MIDDLE: int
    MOUSE_BUTTON_RIGHT: int
    MOUSE_CURSOR_ARROW: int
    MOUSE_CURSOR_HAND: int
    MOUSE_CURSOR_NONE: int
    MOUSE_CURSOR_NOT_ALLOWED: int
    MOUSE_CURSOR_RESIZE_ALL: int
    MOUSE_CURSOR_RESIZE_EW: int
    MOUSE_CURSOR_RESIZE_NESW: int
    MOUSE_CURSOR_RESIZE_NS: int
    MOUSE_CURSOR_RESIZE_NWSE: int
    MOUSE_CURSOR_TEXT_INPUT: int
    NAV_INPUT_ACTIVATE: int
    NAV_INPUT_CANCEL: int
    NAV_INPUT_COUNT: int
    NAV_INPUT_DPAD_DOWN: int
    NAV_INPUT_DPAD_LEFT: int
    NAV_INPUT_DPAD_RIGHT: int
    NAV_INPUT_DPAD_UP: int
    NAV_INPUT_FOCUS_NEXT: int
    NAV_INPUT_FOCUS_PREV: int
    NAV_INPUT_INPUT: int
    NAV_INPUT_L_STICK_DOWN: int
    NAV_INPUT_L_STICK_LEFT: int
    NAV_INPUT_L_STICK_RIGHT: int
    NAV_INPUT_L_STICK_UP: int
    NAV_INPUT_MENU: int
    NAV_INPUT_TWEAK_FAST: int
    NAV_INPUT_TWEAK_SLOW: int
    NONE: int
    ONCE: int
    POPUP_ANY_POPUP: int
    POPUP_ANY_POPUP_ID: int
    POPUP_ANY_POPUP_LEVEL: int
    POPUP_MOUSE_BUTTON_DEFAULT: int
    POPUP_MOUSE_BUTTON_LEFT: int
    POPUP_MOUSE_BUTTON_MASK: int
    POPUP_MOUSE_BUTTON_MIDDLE: int
    POPUP_MOUSE_BUTTON_RIGHT: int
    POPUP_NONE: int
    POPUP_NO_OPEN_OVER_EXISTING_POPUP: int
    POPUP_NO_OPEN_OVER_ITEMS: int
    SELECTABLE_ALLOW_DOUBLE_CLICK: int
    SELECTABLE_ALLOW_ITEM_OVERLAP: int
    SELECTABLE_DISABLED: int
    SELECTABLE_DONT_CLOSE_POPUPS: int
    SELECTABLE_NONE: int
    SELECTABLE_SPAN_ALL_COLUMNS: int
    SLIDER_FLAGS_ALWAYS_CLAMP: int
    SLIDER_FLAGS_LOGARITHMIC: int
    SLIDER_FLAGS_NONE: int
    SLIDER_FLAGS_NO_INPUT: int
    SLIDER_FLAGS_NO_ROUND_TO_FORMAT: int
    SORT_DIRECTION_ASCENDING: int
    SORT_DIRECTION_DESCENDING: int
    SORT_DIRECTION_NONE: int
    STYLE_ALPHA: int
    STYLE_BUTTON_TEXT_ALIGN: int
    STYLE_CELL_PADDING: int
    STYLE_CHILD_BORDERSIZE: int
    STYLE_CHILD_ROUNDING: int
    STYLE_FRAME_BORDERSIZE: int
    STYLE_FRAME_PADDING: int
    STYLE_FRAME_ROUNDING: int
    STYLE_GRAB_MIN_SIZE: int
    STYLE_GRAB_ROUNDING: int
    STYLE_INDENT_SPACING: int
    STYLE_ITEM_INNER_SPACING: int
    STYLE_ITEM_SPACING: int
    STYLE_POPUP_BORDERSIZE: int
    STYLE_POPUP_ROUNDING: int
    STYLE_SCROLLBAR_ROUNDING: int
    STYLE_SCROLLBAR_SIZE: int
    STYLE_SELECTABLE_TEXT_ALIGN: int
    STYLE_TAB_ROUNDING: int
    STYLE_WINDOW_BORDERSIZE: int
    STYLE_WINDOW_MIN_SIZE: int
    STYLE_WINDOW_PADDING: int
    STYLE_WINDOW_ROUNDING: int
    STYLE_WINDOW_TITLE_ALIGN: int
    TABLE_BACKGROUND_TARGET_CELL_BG: int
    TABLE_BACKGROUND_TARGET_NONE: int
    TABLE_BACKGROUND_TARGET_ROW_BG0: int
    TABLE_BACKGROUND_TARGET_ROW_BG1: int
    TABLE_BORDERS: int
    TABLE_BORDERS_HORIZONTAL: int
    TABLE_BORDERS_INNER: int
    TABLE_BORDERS_INNER_HORIZONTAL: int
    TABLE_BORDERS_INNER_VERTICAL: int
    TABLE_BORDERS_OUTER: int
    TABLE_BORDERS_OUTER_HORIZONTAL: int
    TABLE_BORDERS_OUTER_VERTICAL: int
    TABLE_BORDERS_VERTICAL: int
    TABLE_COLUMN_DEFAULT_HIDE: int
    TABLE_COLUMN_DEFAULT_SORT: int
    TABLE_COLUMN_INDENT_DISABLE: int
    TABLE_COLUMN_INDENT_ENABLE: int
    TABLE_COLUMN_IS_ENABLED: int
    TABLE_COLUMN_IS_HOVERED: int
    TABLE_COLUMN_IS_SORTED: int
    TABLE_COLUMN_IS_VISIBLE: int
    TABLE_COLUMN_NONE: int
    TABLE_COLUMN_NO_CLIP: int
    TABLE_COLUMN_NO_HEADER_WIDTH: int
    TABLE_COLUMN_NO_HIDE: int
    TABLE_COLUMN_NO_REORDER: int
    TABLE_COLUMN_NO_RESIZE: int
    TABLE_COLUMN_NO_SORT: int
    TABLE_COLUMN_NO_SORT_ASCENDING: int
    TABLE_COLUMN_NO_SORT_DESCENDING: int
    TABLE_COLUMN_PREFER_SORT_ASCENDING: int
    TABLE_COLUMN_PREFER_SORT_DESCENDING: int
    TABLE_COLUMN_WIDTH_FIXED: int
    TABLE_COLUMN_WIDTH_STRETCH: int
    TABLE_CONTEXT_MENU_IN_BODY: int
    TABLE_HIDEABLE: int
    TABLE_NONE: int
    TABLE_NO_BORDERS_IN_BODY: int
    TABLE_NO_BORDERS_IN_BODY_UTIL_RESIZE: int
    TABLE_NO_CLIP: int
    TABLE_NO_HOST_EXTEND_X: int
    TABLE_NO_HOST_EXTEND_Y: int
    TABLE_NO_KEEP_COLUMNS_VISIBLE: int
    TABLE_NO_PAD_INNER_X: int
    TABLE_NO_PAD_OUTER_X: int
    TABLE_NO_SAVED_SETTINGS: int
    TABLE_PAD_OUTER_X: int
    TABLE_PRECISE_WIDTHS: int
    TABLE_REORDERABLE: int
    TABLE_RESIZABLE: int
    TABLE_ROW_BACKGROUND: int
    TABLE_ROW_HEADERS: int
    TABLE_ROW_NONE: int
    TABLE_SCROLL_X: int
    TABLE_SCROLL_Y: int
    TABLE_SIZING_FIXED_FIT: int
    TABLE_SIZING_FIXED_SAME: int
    TABLE_SIZING_STRETCH_PROP: int
    TABLE_SIZING_STRETCH_SAME: int
    TABLE_SORTABLE: int
    TABLE_SORT_MULTI: int
    TABLE_SORT_TRISTATE: int
    TAB_BAR_AUTO_SELECT_NEW_TABS: int
    TAB_BAR_FITTING_POLICY_DEFAULT: int
    TAB_BAR_FITTING_POLICY_MASK: int
    TAB_BAR_FITTING_POLICY_RESIZE_DOWN: int
    TAB_BAR_FITTING_POLICY_SCROLL: int
    TAB_BAR_NONE: int
    TAB_BAR_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
    TAB_BAR_NO_TAB_LIST_SCROLLING_BUTTONS: int
    TAB_BAR_NO_TOOLTIP: int
    TAB_BAR_REORDERABLE: int
    TAB_BAR_TAB_LIST_POPUP_BUTTON: int
    TAB_ITEM_LEADING: int
    TAB_ITEM_NONE: int
    TAB_ITEM_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
    TAB_ITEM_NO_PUSH_ID: int
    TAB_ITEM_NO_REORDER: int
    TAB_ITEM_NO_TOOLTIP: int
    TAB_ITEM_SET_SELECTED: int
    TAB_ITEM_TRAILING: int
    TAB_ITEM_UNSAVED_DOCUMENT: int
    TREE_NODE_ALLOW_ITEM_OVERLAP: int
    TREE_NODE_BULLET: int
    TREE_NODE_COLLAPSING_HEADER: int
    TREE_NODE_DEFAULT_OPEN: int
    TREE_NODE_FRAMED: int
    TREE_NODE_FRAME_PADDING: int
    TREE_NODE_LEAF: int
    TREE_NODE_NAV_LEFT_JUPS_BACK_HERE: int
    TREE_NODE_NONE: int
    TREE_NODE_NO_AUTO_OPEN_ON_LOG: int
    TREE_NODE_NO_TREE_PUSH_ON_OPEN: int
    TREE_NODE_OPEN_ON_ARROW: int
    TREE_NODE_OPEN_ON_DOUBLE_CLICK: int
    TREE_NODE_SELECTED: int
    TREE_NODE_SPAN_AVAILABLE_WIDTH: int
    TREE_NODE_SPAN_FULL_WIDTH: int
    VERSION: tuple
    VERTEX_BUFFER_COL_OFFSET: int
    VERTEX_BUFFER_POS_OFFSET: int
    VERTEX_BUFFER_UV_OFFSET: int
    VERTEX_SIZE: int
    VIEWPORT_FLAGS_IS_PLATFORM_MONITOR: int
    VIEWPORT_FLAGS_IS_PLATFORM_WINDOW: int
    VIEWPORT_FLAGS_NONE: int
    VIEWPORT_FLAGS_OWNED_BY_APP: int
    WINDOW_ALWAYS_AUTO_RESIZE: int
    WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR: int
    WINDOW_ALWAYS_USE_WINDOW_PADDING: int
    WINDOW_ALWAYS_VERTICAL_SCROLLBAR: int
    WINDOW_HORIZONTAL_SCROLLING_BAR: int
    WINDOW_MENU_BAR: int
    WINDOW_NONE: int
    WINDOW_NO_BACKGROUND: int
    WINDOW_NO_BRING_TO_FRONT_ON_FOCUS: int
    WINDOW_NO_COLLAPSE: int
    WINDOW_NO_DECORATION: int
    WINDOW_NO_FOCUS_ON_APPEARING: int
    WINDOW_NO_INPUTS: int
    WINDOW_NO_MOUSE_INPUTS: int
    WINDOW_NO_MOVE: int
    WINDOW_NO_NAV: int
    WINDOW_NO_NAV_FOCUS: int
    WINDOW_NO_NAV_INPUTS: int
    WINDOW_NO_RESIZE: int
    WINDOW_NO_SAVED_SETTINGS: int
    WINDOW_NO_SCROLLBAR: int
    WINDOW_NO_SCROLL_WITH_MOUSE: int
    WINDOW_NO_TITLE_BAR: int
    WINDOW_UNSAVED_DOCUMENT: int

    @staticmethod
    def accept_drag_drop_payload(): ...

    @staticmethod
    def align_text_to_frame_padding(): ...

    @staticmethod
    def arrow_button(): ...

    @staticmethod
    def begin(): ...

    @staticmethod
    def begin_child(label, width=0, height=0, border=False, flags=0): ...

    @staticmethod
    def begin_combo(): ...

    @staticmethod
    def begin_drag_drop_source(): ...

    @staticmethod
    def begin_drag_drop_target(): ...

    @staticmethod
    def begin_group(): ...

    @staticmethod
    def begin_list_box(): ...

    @staticmethod
    def begin_main_menu_bar(): ...

    @staticmethod
    def begin_menu(): ...

    @staticmethod
    def begin_menu_bar(): ...

    @staticmethod
    def begin_popup(): ...

    @staticmethod
    def begin_popup_context_item(): ...

    @staticmethod
    def begin_popup_context_void(): ...

    @staticmethod
    def begin_popup_context_window(): ...

    @staticmethod
    def begin_popup_modal(): ...

    @staticmethod
    def begin_tab_bar(): ...

    @staticmethod
    def begin_tab_item(): ...

    @staticmethod
    def begin_table(): ...

    @staticmethod
    def begin_tooltip(): ...

    @staticmethod
    def bullet(): ...

    @staticmethod
    def bullet_text(): ...

    @staticmethod
    def button(): ...

    @staticmethod
    def calc_text_size(): ...

    @staticmethod
    def calculate_item_width(): ...

    @staticmethod
    def capture_mouse_from_app(): ...

    @staticmethod
    def checkbox(): ...

    @staticmethod
    def checkbox_flags(): ...

    @staticmethod
    def close_current_popup(): ...

    @staticmethod
    def collapsing_header(): ...

    @staticmethod
    def color_button(): ...

    @staticmethod
    def color_convert_float4_to_u32(): ...

    @staticmethod
    def color_convert_hsv_to_rgb(): ...

    @staticmethod
    def color_convert_rgb_to_hsv(): ...

    @staticmethod
    def color_convert_u32_to_float4(): ...

    @staticmethod
    def color_edit3(): ...

    @staticmethod
    def color_edit4(): ...

    @staticmethod
    def colored(variable, r, g, b, a=1.0): ...

    @staticmethod
    def columns(): ...

    @staticmethod
    def combo(): ...

    @staticmethod
    def contextmanager(func): ...

    @staticmethod
    def create_context(): ...

    @staticmethod
    def destroy_context(): ...

    @staticmethod
    def drag_float(): ...

    @staticmethod
    def drag_float2(): ...

    @staticmethod
    def drag_float3(): ...

    @staticmethod
    def drag_float4(): ...

    @staticmethod
    def drag_float_range2(): ...

    @staticmethod
    def drag_int(): ...

    @staticmethod
    def drag_int2(): ...

    @staticmethod
    def drag_int3(): ...

    @staticmethod
    def drag_int4(): ...

    @staticmethod
    def drag_int_range2(): ...

    @staticmethod
    def drag_scalar(): ...

    @staticmethod
    def drag_scalar_N(): ...

    @staticmethod
    def dummy(): ...

    @staticmethod
    def end(): ...

    @staticmethod
    def end_child(): ...

    @staticmethod
    def end_combo(): ...

    @staticmethod
    def end_drag_drop_source(): ...

    @staticmethod
    def end_drag_drop_target(): ...

    @staticmethod
    def end_frame(): ...

    @staticmethod
    def end_group(): ...

    @staticmethod
    def end_list_box(): ...

    @staticmethod
    def end_main_menu_bar(): ...

    @staticmethod
    def end_menu(): ...

    @staticmethod
    def end_menu_bar(): ...

    @staticmethod
    def end_popup(): ...

    @staticmethod
    def end_tab_bar(): ...

    @staticmethod
    def end_tab_item(): ...

    @staticmethod
    def end_table(): ...

    @staticmethod
    def end_tooltip(): ...

    @staticmethod
    def font(font): ...

    @staticmethod
    def get_background_draw_list(): ...

    @staticmethod
    def get_clipboard_text(): ...

    @staticmethod
    def get_color_u32(): ...

    @staticmethod
    def get_color_u32_idx(): ...

    @staticmethod
    def get_color_u32_rgba(): ...

    @staticmethod
    def get_column_index(): ...

    @staticmethod
    def get_column_offset(): ...

    @staticmethod
    def get_column_width(): ...

    @staticmethod
    def get_columns_count(): ...

    @staticmethod
    def get_content_region_available(): ...

    @staticmethod
    def get_content_region_available_width(): ...

    @staticmethod
    def get_content_region_max(): ...

    @staticmethod
    def get_current_context(): ...

    @staticmethod
    def get_cursor_pos(): ...

    @staticmethod
    def get_cursor_pos_x(): ...

    @staticmethod
    def get_cursor_pos_y(): ...

    @staticmethod
    def get_cursor_position(): ...

    @staticmethod
    def get_cursor_screen_pos(): ...

    @staticmethod
    def get_cursor_screen_position(): ...

    @staticmethod
    def get_cursor_start_pos(): ...

    @staticmethod
    def get_cursor_start_position(): ...

    @staticmethod
    def get_drag_drop_payload(): ...

    @staticmethod
    def get_draw_data(): ...

    @staticmethod
    def get_font_size(): ...

    @staticmethod
    def get_font_tex_uv_white_pixel(): ...

    @staticmethod
    def get_foreground_draw_list(): ...

    @staticmethod
    def get_frame_height(): ...

    @staticmethod
    def get_frame_height_with_spacing(): ...

    @staticmethod
    def get_io(): ...

    @staticmethod
    def get_item_rect_max(): ...

    @staticmethod
    def get_item_rect_min(): ...

    @staticmethod
    def get_item_rect_size(): ...

    @staticmethod
    def get_key_index(): ...

    @staticmethod
    def get_main_viewport(): ...

    @staticmethod
    def get_mouse_cursor(): ...

    @staticmethod
    def get_mouse_drag_delta(): ...

    @staticmethod
    def get_mouse_pos(): ...

    @staticmethod
    def get_mouse_position(): ...

    @staticmethod
    def get_overlay_draw_list(): ...

    @staticmethod
    def get_scroll_max_x(): ...

    @staticmethod
    def get_scroll_max_y(): ...

    @staticmethod
    def get_scroll_x(): ...

    @staticmethod
    def get_scroll_y(): ...

    @staticmethod
    def get_style(): ...

    @staticmethod
    def get_style_color_name(): ...

    @staticmethod
    def get_style_color_vec_4(): ...

    @staticmethod
    def get_text_line_height(): ...

    @staticmethod
    def get_text_line_height_with_spacing(): ...

    @staticmethod
    def get_time(): ...

    @staticmethod
    def get_tree_node_to_label_spacing(): ...

    @staticmethod
    def get_version(): ...

    @staticmethod
    def get_window_content_region_max(): ...

    @staticmethod
    def get_window_content_region_min(): ...

    @staticmethod
    def get_window_content_region_width(): ...

    @staticmethod
    def get_window_draw_list(): ...

    @staticmethod
    def get_window_height(): ...

    @staticmethod
    def get_window_position(): ...

    @staticmethod
    def get_window_size(): ...

    @staticmethod
    def get_window_width(): ...

    @staticmethod
    def image(): ...

    @staticmethod
    def image_button(): ...

    @staticmethod
    def indent(): ...

    @staticmethod
    def index_buffer_index_size(): ...

    @staticmethod
    def input_double(): ...

    @staticmethod
    def input_float(): ...

    @staticmethod
    def input_float2(): ...

    @staticmethod
    def input_float3(): ...

    @staticmethod
    def input_float4(): ...

    @staticmethod
    def input_int(): ...

    @staticmethod
    def input_int2(): ...

    @staticmethod
    def input_int3(): ...

    @staticmethod
    def input_int4(): ...

    @staticmethod
    def input_scalar(): ...

    @staticmethod
    def input_scalar_N(): ...

    @staticmethod
    def input_text(): ...

    @staticmethod
    def input_text_multiline(): ...

    @staticmethod
    def input_text_with_hint(): ...

    @staticmethod
    def invisible_button(): ...

    @staticmethod
    def is_any_item_active(): ...

    @staticmethod
    def is_any_item_focused(): ...

    @staticmethod
    def is_any_item_hovered(): ...

    @staticmethod
    def is_item_activated(): ...

    @staticmethod
    def is_item_active(): ...

    @staticmethod
    def is_item_clicked(): ...

    @staticmethod
    def is_item_deactivated(): ...

    @staticmethod
    def is_item_deactivated_after_edit(): ...

    @staticmethod
    def is_item_edited(): ...

    @staticmethod
    def is_item_focused(): ...

    @staticmethod
    def is_item_hovered(): ...

    @staticmethod
    def is_item_toggled_open(): ...

    @staticmethod
    def is_item_visible(): ...

    @staticmethod
    def is_key_down(): ...

    @staticmethod
    def is_key_pressed(): ...

    @staticmethod
    def is_mouse_clicked(): ...

    @staticmethod
    def is_mouse_double_clicked(): ...

    @staticmethod
    def is_mouse_down(): ...

    @staticmethod
    def is_mouse_dragging(): ...

    @staticmethod
    def is_mouse_hovering_rect(): ...

    @staticmethod
    def is_mouse_released(): ...

    @staticmethod
    def is_popup_open(): ...

    @staticmethod
    def is_rect_visible(): ...

    @staticmethod
    def is_window_appearing(): ...

    @staticmethod
    def is_window_collapsed(): ...

    @staticmethod
    def is_window_focused(): ...

    @staticmethod
    def is_window_hovered(): ...

    @staticmethod
    def istyled(*variables_and_values): ...

    @staticmethod
    def label_text(): ...

    @staticmethod
    def listbox(): ...

    @staticmethod
    def listbox_footer(): ...

    @staticmethod
    def listbox_header(): ...

    @staticmethod
    def load_ini_settings_from_disk(): ...

    @staticmethod
    def load_ini_settings_from_memory(): ...

    @staticmethod
    def menu_item(): ...

    @staticmethod
    def namedtuple(typename, field_names, rename=False, defaults=None, module=None): ...

    @staticmethod
    def new_frame(): ...

    @staticmethod
    def new_line(): ...

    @staticmethod
    def next_column(): ...

    @staticmethod
    def open_popup(): ...

    @staticmethod
    def open_popup_on_item_click(): ...

    @staticmethod
    def plot_histogram(): ...

    @staticmethod
    def plot_lines(): ...

    @staticmethod
    def pop_allow_keyboard_focus(): ...

    @staticmethod
    def pop_button_repeat(): ...

    @staticmethod
    def pop_clip_rect(): ...

    @staticmethod
    def pop_font(): ...

    @staticmethod
    def pop_id(): ...

    @staticmethod
    def pop_item_width(): ...

    @staticmethod
    def pop_style_color(): ...

    @staticmethod
    def pop_style_var(): ...

    @staticmethod
    def pop_text_wrap_pos(): ...

    @staticmethod
    def pop_text_wrap_position(): ...

    @staticmethod
    def progress_bar(): ...

    @staticmethod
    def push_allow_keyboard_focus(): ...

    @staticmethod
    def push_button_repeat(): ...

    @staticmethod
    def push_clip_rect(): ...

    @staticmethod
    def push_font(): ...

    @staticmethod
    def push_id(): ...

    @staticmethod
    def push_item_width(): ...

    @staticmethod
    def push_style_color(): ...

    @staticmethod
    def push_style_var(): ...

    @staticmethod
    def push_text_wrap_pos(): ...

    @staticmethod
    def push_text_wrap_position(): ...

    @staticmethod
    def radio_button(): ...

    @staticmethod
    def render(): ...

    @staticmethod
    def reset_mouse_drag_delta(): ...

    @staticmethod
    def same_line(): ...

    @staticmethod
    def save_ini_settings_to_disk(): ...

    @staticmethod
    def save_ini_settings_to_memory(): ...

    @staticmethod
    def selectable(): ...

    @staticmethod
    def separator(): ...

    @staticmethod
    def set_clipboard_text(): ...

    @staticmethod
    def set_column_offset(): ...

    @staticmethod
    def set_column_width(): ...

    @staticmethod
    def set_current_context(): ...

    @staticmethod
    def set_cursor_pos(): ...

    @staticmethod
    def set_cursor_pos_x(): ...

    @staticmethod
    def set_cursor_pos_y(): ...

    @staticmethod
    def set_cursor_position(): ...

    @staticmethod
    def set_cursor_screen_pos(): ...

    @staticmethod
    def set_cursor_screen_position(): ...

    @staticmethod
    def set_drag_drop_payload(): ...

    @staticmethod
    def set_item_allow_overlap(): ...

    @staticmethod
    def set_item_default_focus(): ...

    @staticmethod
    def set_keyboard_focus_here(): ...

    @staticmethod
    def set_mouse_cursor(): ...

    @staticmethod
    def set_next_item_open(): ...

    @staticmethod
    def set_next_item_width(): ...

    @staticmethod
    def set_next_window_bg_alpha(): ...

    @staticmethod
    def set_next_window_collapsed(): ...

    @staticmethod
    def set_next_window_content_size(): ...

    @staticmethod
    def set_next_window_focus(): ...

    @staticmethod
    def set_next_window_position(): ...

    @staticmethod
    def set_next_window_size(): ...

    @staticmethod
    def set_next_window_size_constraints(): ...

    @staticmethod
    def set_scroll_from_pos_x(): ...

    @staticmethod
    def set_scroll_from_pos_y(): ...

    @staticmethod
    def set_scroll_here_x(): ...

    @staticmethod
    def set_scroll_here_y(): ...

    @staticmethod
    def set_scroll_x(): ...

    @staticmethod
    def set_scroll_y(): ...

    @staticmethod
    def set_tab_item_closed(): ...

    @staticmethod
    def set_tooltip(): ...

    @staticmethod
    def set_window_collapsed(): ...

    @staticmethod
    def set_window_collapsed_labeled(): ...

    @staticmethod
    def set_window_focus(): ...

    @staticmethod
    def set_window_focus_labeled(): ...

    @staticmethod
    def set_window_font_scale(): ...

    @staticmethod
    def set_window_position(): ...

    @staticmethod
    def set_window_position_labeled(): ...

    @staticmethod
    def set_window_size(): ...

    @staticmethod
    def set_window_size_named(): ...

    @staticmethod
    def show_about_window(): ...

    @staticmethod
    def show_demo_window(): ...

    @staticmethod
    def show_font_selector(): ...

    @staticmethod
    def show_metrics_window(): ...

    @staticmethod
    def show_style_editor(): ...

    @staticmethod
    def show_style_selector(): ...

    @staticmethod
    def show_test_window(): ...

    @staticmethod
    def show_user_guide(): ...

    @staticmethod
    def slider_angle(): ...

    @staticmethod
    def slider_float(): ...

    @staticmethod
    def slider_float2(): ...

    @staticmethod
    def slider_float3(): ...

    @staticmethod
    def slider_float4(): ...

    @staticmethod
    def slider_int(): ...

    @staticmethod
    def slider_int2(): ...

    @staticmethod
    def slider_int3(): ...

    @staticmethod
    def slider_int4(): ...

    @staticmethod
    def slider_scalar(): ...

    @staticmethod
    def slider_scalar_N(): ...

    @staticmethod
    def small_button(): ...

    @staticmethod
    def spacing(): ...

    @staticmethod
    def style_colors_classic(): ...

    @staticmethod
    def style_colors_dark(): ...

    @staticmethod
    def style_colors_light(): ...

    @staticmethod
    def styled(variable, value): ...

    @staticmethod
    def tab_item_button(): ...

    @staticmethod
    def table_get_column_count(): ...

    @staticmethod
    def table_get_column_flags(): ...

    @staticmethod
    def table_get_column_index(): ...

    @staticmethod
    def table_get_column_name(): ...

    @staticmethod
    def table_get_row_index(): ...

    @staticmethod
    def table_get_sort_specs(): ...

    @staticmethod
    def table_header(): ...

    @staticmethod
    def table_headers_row(): ...

    @staticmethod
    def table_next_column(): ...

    @staticmethod
    def table_next_row(): ...

    @staticmethod
    def table_set_background_color(): ...

    @staticmethod
    def table_set_column_index(): ...

    @staticmethod
    def table_setup_column(): ...

    @staticmethod
    def table_setup_scroll_freeze(): ...

    @staticmethod
    def text(): ...

    @staticmethod
    def text_ansi(): ...

    @staticmethod
    def text_ansi_colored(): ...

    @staticmethod
    def text_colored(): ...

    @staticmethod
    def text_disabled(): ...

    @staticmethod
    def text_unformatted(): ...

    @staticmethod
    def text_wrapped(): ...

    @staticmethod
    def tree_node(): ...

    @staticmethod
    def tree_pop(): ...

    @staticmethod
    def unindent(): ...

    @staticmethod
    def v_slider_float(): ...

    @staticmethod
    def v_slider_int(): ...

    @staticmethod
    def v_slider_scalar(): ...

    @staticmethod
    def vertex_buffer_vertex_col_offset(): ...

    @staticmethod
    def vertex_buffer_vertex_pos_offset(): ...

    @staticmethod
    def vertex_buffer_vertex_size(): ...

    @staticmethod
    def vertex_buffer_vertex_uv_offset(): ...

    class _compat:
      @staticmethod
      def deprecated(reason): ...

      @staticmethod
      def warn(): ...

      @staticmethod
      def wraps(wrapped, assigned=('__module__', '__name__', '__qualname__', '__doc__', '__annotations__', '__type_params__'), updated=('__dict__',)): ...

      class ImguiDeprecationWarning:
        args: args

        @staticmethod
        def add_note(): ...

        @staticmethod
        def with_traceback(): ...

    class core:
      ALWAYS: int
      APPEARING: int
      BACKEND_HAS_GAMEPAD: int
      BACKEND_HAS_MOUSE_CURSORS: int
      BACKEND_HAS_SET_MOUSE_POS: int
      BACKEND_NONE: int
      BACKEND_RENDERER_HAS_VTX_OFFSET: int
      BUTTON_MOUSE_BUTTON_LEFT: int
      BUTTON_MOUSE_BUTTON_MIDDLE: int
      BUTTON_MOUSE_BUTTON_RIGHT: int
      BUTTON_NONE: int
      COLOR_BORDER: int
      COLOR_BORDER_SHADOW: int
      COLOR_BUTTON: int
      COLOR_BUTTON_ACTIVE: int
      COLOR_BUTTON_HOVERED: int
      COLOR_CHECK_MARK: int
      COLOR_CHILD_BACKGROUND: int
      COLOR_COUNT: int
      COLOR_DRAG_DROP_TARGET: int
      COLOR_EDIT_ALPHA_BAR: int
      COLOR_EDIT_ALPHA_PREVIEW: int
      COLOR_EDIT_ALPHA_PREVIEW_HALF: int
      COLOR_EDIT_DEFAULT_OPTIONS: int
      COLOR_EDIT_DISPLAY_HEX: int
      COLOR_EDIT_DISPLAY_HSV: int
      COLOR_EDIT_DISPLAY_RGB: int
      COLOR_EDIT_FLOAT: int
      COLOR_EDIT_HDR: int
      COLOR_EDIT_INPUT_HSV: int
      COLOR_EDIT_INPUT_RGB: int
      COLOR_EDIT_NONE: int
      COLOR_EDIT_NO_ALPHA: int
      COLOR_EDIT_NO_BORDER: int
      COLOR_EDIT_NO_DRAG_DROP: int
      COLOR_EDIT_NO_INPUTS: int
      COLOR_EDIT_NO_LABEL: int
      COLOR_EDIT_NO_OPTIONS: int
      COLOR_EDIT_NO_PICKER: int
      COLOR_EDIT_NO_SIDE_PREVIEW: int
      COLOR_EDIT_NO_SMALL_PREVIEW: int
      COLOR_EDIT_NO_TOOLTIP: int
      COLOR_EDIT_PICKER_HUE_BAR: int
      COLOR_EDIT_PICKER_HUE_WHEEL: int
      COLOR_EDIT_UINT8: int
      COLOR_FRAME_BACKGROUND: int
      COLOR_FRAME_BACKGROUND_ACTIVE: int
      COLOR_FRAME_BACKGROUND_HOVERED: int
      COLOR_HEADER: int
      COLOR_HEADER_ACTIVE: int
      COLOR_HEADER_HOVERED: int
      COLOR_MENUBAR_BACKGROUND: int
      COLOR_MODAL_WINDOW_DIM_BACKGROUND: int
      COLOR_NAV_HIGHLIGHT: int
      COLOR_NAV_WINDOWING_DIM_BACKGROUND: int
      COLOR_NAV_WINDOWING_HIGHLIGHT: int
      COLOR_PLOT_HISTOGRAM: int
      COLOR_PLOT_HISTOGRAM_HOVERED: int
      COLOR_PLOT_LINES: int
      COLOR_PLOT_LINES_HOVERED: int
      COLOR_POPUP_BACKGROUND: int
      COLOR_RESIZE_GRIP: int
      COLOR_RESIZE_GRIP_ACTIVE: int
      COLOR_RESIZE_GRIP_HOVERED: int
      COLOR_SCROLLBAR_BACKGROUND: int
      COLOR_SCROLLBAR_GRAB: int
      COLOR_SCROLLBAR_GRAB_ACTIVE: int
      COLOR_SCROLLBAR_GRAB_HOVERED: int
      COLOR_SEPARATOR: int
      COLOR_SEPARATOR_ACTIVE: int
      COLOR_SEPARATOR_HOVERED: int
      COLOR_SLIDER_GRAB: int
      COLOR_SLIDER_GRAB_ACTIVE: int
      COLOR_TAB: int
      COLOR_TABLE_BORDER_LIGHT: int
      COLOR_TABLE_BORDER_STRONG: int
      COLOR_TABLE_HEADER_BACKGROUND: int
      COLOR_TABLE_ROW_BACKGROUND: int
      COLOR_TABLE_ROW_BACKGROUND_ALT: int
      COLOR_TAB_ACTIVE: int
      COLOR_TAB_HOVERED: int
      COLOR_TAB_UNFOCUSED: int
      COLOR_TAB_UNFOCUSED_ACTIVE: int
      COLOR_TEXT: int
      COLOR_TEXT_DISABLED: int
      COLOR_TEXT_SELECTED_BACKGROUND: int
      COLOR_TITLE_BACKGROUND: int
      COLOR_TITLE_BACKGROUND_ACTIVE: int
      COLOR_TITLE_BACKGROUND_COLLAPSED: int
      COLOR_WINDOW_BACKGROUND: int
      COMBO_HEIGHT_LARGE: int
      COMBO_HEIGHT_LARGEST: int
      COMBO_HEIGHT_MASK: int
      COMBO_HEIGHT_REGULAR: int
      COMBO_HEIGHT_SMALL: int
      COMBO_NONE: int
      COMBO_NO_ARROW_BUTTON: int
      COMBO_NO_PREVIEW: int
      COMBO_POPUP_ALIGN_LEFT: int
      CONFIG_IS_RGB: int
      CONFIG_IS_TOUCH_SCREEN: int
      CONFIG_NAV_ENABLE_GAMEPAD: int
      CONFIG_NAV_ENABLE_KEYBOARD: int
      CONFIG_NAV_ENABLE_SET_MOUSE_POS: int
      CONFIG_NAV_NO_CAPTURE_KEYBOARD: int
      CONFIG_NONE: int
      CONFIG_NO_MOUSE: int
      CONFIG_NO_MOUSE_CURSOR_CHANGE: int
      DATA_TYPE_DOUBLE: int
      DATA_TYPE_FLOAT: int
      DATA_TYPE_S16: int
      DATA_TYPE_S32: int
      DATA_TYPE_S64: int
      DATA_TYPE_S8: int
      DATA_TYPE_U16: int
      DATA_TYPE_U32: int
      DATA_TYPE_U64: int
      DATA_TYPE_U8: int
      DIRECTION_DOWN: int
      DIRECTION_LEFT: int
      DIRECTION_NONE: int
      DIRECTION_RIGHT: int
      DIRECTION_UP: int
      DRAG_DROP_ACCEPT_BEFORE_DELIVERY: int
      DRAG_DROP_ACCEPT_NO_DRAW_DEFAULT_RECT: int
      DRAG_DROP_ACCEPT_NO_PREVIEW_TOOLTIP: int
      DRAG_DROP_ACCEPT_PEEK_ONLY: int
      DRAG_DROP_NONE: int
      DRAG_DROP_SOURCE_ALLOW_NULL_ID: int
      DRAG_DROP_SOURCE_AUTO_EXPIRE_PAYLOAD: int
      DRAG_DROP_SOURCE_EXTERN: int
      DRAG_DROP_SOURCE_NO_DISABLE_HOVER: int
      DRAG_DROP_SOURCE_NO_HOLD_TO_OPEN_OTHERS: int
      DRAG_DROP_SOURCE_NO_PREVIEW_TOOLTIP: int
      DRAW_CLOSED: int
      DRAW_CORNER_ALL: int
      DRAW_CORNER_BOTTOM: int
      DRAW_CORNER_BOTTOM_LEFT: int
      DRAW_CORNER_BOTTOM_RIGHT: int
      DRAW_CORNER_LEFT: int
      DRAW_CORNER_NONE: int
      DRAW_CORNER_RIGHT: int
      DRAW_CORNER_TOP: int
      DRAW_CORNER_TOP_LEFT: int
      DRAW_CORNER_TOP_RIGHT: int
      DRAW_LIST_ALLOW_VTX_OFFSET: int
      DRAW_LIST_ANTI_ALIASED_FILL: int
      DRAW_LIST_ANTI_ALIASED_LINES: int
      DRAW_LIST_ANTI_ALIASED_LINES_USE_TEX: int
      DRAW_LIST_NONE: int
      DRAW_NONE: int
      DRAW_ROUND_CORNERS_ALL: int
      DRAW_ROUND_CORNERS_BOTTOM: int
      DRAW_ROUND_CORNERS_BOTTOM_LEFT: int
      DRAW_ROUND_CORNERS_BOTTOM_RIGHT: int
      DRAW_ROUND_CORNERS_LEFT: int
      DRAW_ROUND_CORNERS_NONE: int
      DRAW_ROUND_CORNERS_RIGHT: int
      DRAW_ROUND_CORNERS_TOP: int
      DRAW_ROUND_CORNERS_TOP_LEFT: int
      DRAW_ROUND_CORNERS_TOP_RIGHT: int
      FIRST_USE_EVER: int
      FLOAT_MAX: float
      FLOAT_MIN: float
      FOCUS_ANY_WINDOW: int
      FOCUS_CHILD_WINDOWS: int
      FOCUS_NONE: int
      FOCUS_ROOT_AND_CHILD_WINDOWS: int
      FOCUS_ROOT_WINDOW: int
      FONT_ATLAS_NONE: int
      FONT_ATLAS_NO_BAKED_LINES: int
      FONT_ATLAS_NO_MOUSE_CURSOR: int
      FONT_ATLAS_NO_POWER_OF_TWO_HEIGHT: int
      HOVERED_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM: int
      HOVERED_ALLOW_WHEN_BLOCKED_BY_POPUP: int
      HOVERED_ALLOW_WHEN_DISABLED: int
      HOVERED_ALLOW_WHEN_OVERLAPPED: int
      HOVERED_ANY_WINDOW: int
      HOVERED_CHILD_WINDOWS: int
      HOVERED_NONE: int
      HOVERED_RECT_ONLY: int
      HOVERED_ROOT_AND_CHILD_WINDOWS: int
      HOVERED_ROOT_WINDOW: int
      INPUT_TEXT_ALLOW_TAB_INPUT: int
      INPUT_TEXT_ALWAYS_INSERT_MODE: int
      INPUT_TEXT_ALWAYS_OVERWRITE: int
      INPUT_TEXT_AUTO_SELECT_ALL: int
      INPUT_TEXT_CALLBACK_ALWAYS: int
      INPUT_TEXT_CALLBACK_CHAR_FILTER: int
      INPUT_TEXT_CALLBACK_COMPLETION: int
      INPUT_TEXT_CALLBACK_EDIT: int
      INPUT_TEXT_CALLBACK_HISTORY: int
      INPUT_TEXT_CALLBACK_RESIZE: int
      INPUT_TEXT_CHARS_DECIMAL: int
      INPUT_TEXT_CHARS_HEXADECIMAL: int
      INPUT_TEXT_CHARS_NO_BLANK: int
      INPUT_TEXT_CHARS_SCIENTIFIC: int
      INPUT_TEXT_CHARS_UPPERCASE: int
      INPUT_TEXT_CTRL_ENTER_FOR_NEW_LINE: int
      INPUT_TEXT_ENTER_RETURNS_TRUE: int
      INPUT_TEXT_NONE: int
      INPUT_TEXT_NO_HORIZONTAL_SCROLL: int
      INPUT_TEXT_NO_UNDO_REDO: int
      INPUT_TEXT_PASSWORD: int
      INPUT_TEXT_READ_ONLY: int
      KEY_A: int
      KEY_BACKSPACE: int
      KEY_C: int
      KEY_DELETE: int
      KEY_DOWN_ARROW: int
      KEY_END: int
      KEY_ENTER: int
      KEY_ESCAPE: int
      KEY_HOME: int
      KEY_INSERT: int
      KEY_LEFT_ARROW: int
      KEY_MOD_ALT: int
      KEY_MOD_CTRL: int
      KEY_MOD_NONE: int
      KEY_MOD_SHIFT: int
      KEY_MOD_SUPER: int
      KEY_PAD_ENTER: int
      KEY_PAGE_DOWN: int
      KEY_PAGE_UP: int
      KEY_RIGHT_ARROW: int
      KEY_SPACE: int
      KEY_TAB: int
      KEY_UP_ARROW: int
      KEY_V: int
      KEY_X: int
      KEY_Y: int
      KEY_Z: int
      MOUSE_BUTTON_LEFT: int
      MOUSE_BUTTON_MIDDLE: int
      MOUSE_BUTTON_RIGHT: int
      MOUSE_CURSOR_ARROW: int
      MOUSE_CURSOR_HAND: int
      MOUSE_CURSOR_NONE: int
      MOUSE_CURSOR_NOT_ALLOWED: int
      MOUSE_CURSOR_RESIZE_ALL: int
      MOUSE_CURSOR_RESIZE_EW: int
      MOUSE_CURSOR_RESIZE_NESW: int
      MOUSE_CURSOR_RESIZE_NS: int
      MOUSE_CURSOR_RESIZE_NWSE: int
      MOUSE_CURSOR_TEXT_INPUT: int
      NAV_INPUT_ACTIVATE: int
      NAV_INPUT_CANCEL: int
      NAV_INPUT_COUNT: int
      NAV_INPUT_DPAD_DOWN: int
      NAV_INPUT_DPAD_LEFT: int
      NAV_INPUT_DPAD_RIGHT: int
      NAV_INPUT_DPAD_UP: int
      NAV_INPUT_FOCUS_NEXT: int
      NAV_INPUT_FOCUS_PREV: int
      NAV_INPUT_INPUT: int
      NAV_INPUT_L_STICK_DOWN: int
      NAV_INPUT_L_STICK_LEFT: int
      NAV_INPUT_L_STICK_RIGHT: int
      NAV_INPUT_L_STICK_UP: int
      NAV_INPUT_MENU: int
      NAV_INPUT_TWEAK_FAST: int
      NAV_INPUT_TWEAK_SLOW: int
      NONE: int
      ONCE: int
      POPUP_ANY_POPUP: int
      POPUP_ANY_POPUP_ID: int
      POPUP_ANY_POPUP_LEVEL: int
      POPUP_MOUSE_BUTTON_DEFAULT: int
      POPUP_MOUSE_BUTTON_LEFT: int
      POPUP_MOUSE_BUTTON_MASK: int
      POPUP_MOUSE_BUTTON_MIDDLE: int
      POPUP_MOUSE_BUTTON_RIGHT: int
      POPUP_NONE: int
      POPUP_NO_OPEN_OVER_EXISTING_POPUP: int
      POPUP_NO_OPEN_OVER_ITEMS: int
      SELECTABLE_ALLOW_DOUBLE_CLICK: int
      SELECTABLE_ALLOW_ITEM_OVERLAP: int
      SELECTABLE_DISABLED: int
      SELECTABLE_DONT_CLOSE_POPUPS: int
      SELECTABLE_NONE: int
      SELECTABLE_SPAN_ALL_COLUMNS: int
      SLIDER_FLAGS_ALWAYS_CLAMP: int
      SLIDER_FLAGS_LOGARITHMIC: int
      SLIDER_FLAGS_NONE: int
      SLIDER_FLAGS_NO_INPUT: int
      SLIDER_FLAGS_NO_ROUND_TO_FORMAT: int
      SORT_DIRECTION_ASCENDING: int
      SORT_DIRECTION_DESCENDING: int
      SORT_DIRECTION_NONE: int
      STYLE_ALPHA: int
      STYLE_BUTTON_TEXT_ALIGN: int
      STYLE_CELL_PADDING: int
      STYLE_CHILD_BORDERSIZE: int
      STYLE_CHILD_ROUNDING: int
      STYLE_FRAME_BORDERSIZE: int
      STYLE_FRAME_PADDING: int
      STYLE_FRAME_ROUNDING: int
      STYLE_GRAB_MIN_SIZE: int
      STYLE_GRAB_ROUNDING: int
      STYLE_INDENT_SPACING: int
      STYLE_ITEM_INNER_SPACING: int
      STYLE_ITEM_SPACING: int
      STYLE_POPUP_BORDERSIZE: int
      STYLE_POPUP_ROUNDING: int
      STYLE_SCROLLBAR_ROUNDING: int
      STYLE_SCROLLBAR_SIZE: int
      STYLE_SELECTABLE_TEXT_ALIGN: int
      STYLE_TAB_ROUNDING: int
      STYLE_WINDOW_BORDERSIZE: int
      STYLE_WINDOW_MIN_SIZE: int
      STYLE_WINDOW_PADDING: int
      STYLE_WINDOW_ROUNDING: int
      STYLE_WINDOW_TITLE_ALIGN: int
      TABLE_BACKGROUND_TARGET_CELL_BG: int
      TABLE_BACKGROUND_TARGET_NONE: int
      TABLE_BACKGROUND_TARGET_ROW_BG0: int
      TABLE_BACKGROUND_TARGET_ROW_BG1: int
      TABLE_BORDERS: int
      TABLE_BORDERS_HORIZONTAL: int
      TABLE_BORDERS_INNER: int
      TABLE_BORDERS_INNER_HORIZONTAL: int
      TABLE_BORDERS_INNER_VERTICAL: int
      TABLE_BORDERS_OUTER: int
      TABLE_BORDERS_OUTER_HORIZONTAL: int
      TABLE_BORDERS_OUTER_VERTICAL: int
      TABLE_BORDERS_VERTICAL: int
      TABLE_COLUMN_DEFAULT_HIDE: int
      TABLE_COLUMN_DEFAULT_SORT: int
      TABLE_COLUMN_INDENT_DISABLE: int
      TABLE_COLUMN_INDENT_ENABLE: int
      TABLE_COLUMN_IS_ENABLED: int
      TABLE_COLUMN_IS_HOVERED: int
      TABLE_COLUMN_IS_SORTED: int
      TABLE_COLUMN_IS_VISIBLE: int
      TABLE_COLUMN_NONE: int
      TABLE_COLUMN_NO_CLIP: int
      TABLE_COLUMN_NO_HEADER_WIDTH: int
      TABLE_COLUMN_NO_HIDE: int
      TABLE_COLUMN_NO_REORDER: int
      TABLE_COLUMN_NO_RESIZE: int
      TABLE_COLUMN_NO_SORT: int
      TABLE_COLUMN_NO_SORT_ASCENDING: int
      TABLE_COLUMN_NO_SORT_DESCENDING: int
      TABLE_COLUMN_PREFER_SORT_ASCENDING: int
      TABLE_COLUMN_PREFER_SORT_DESCENDING: int
      TABLE_COLUMN_WIDTH_FIXED: int
      TABLE_COLUMN_WIDTH_STRETCH: int
      TABLE_CONTEXT_MENU_IN_BODY: int
      TABLE_HIDEABLE: int
      TABLE_NONE: int
      TABLE_NO_BORDERS_IN_BODY: int
      TABLE_NO_BORDERS_IN_BODY_UTIL_RESIZE: int
      TABLE_NO_CLIP: int
      TABLE_NO_HOST_EXTEND_X: int
      TABLE_NO_HOST_EXTEND_Y: int
      TABLE_NO_KEEP_COLUMNS_VISIBLE: int
      TABLE_NO_PAD_INNER_X: int
      TABLE_NO_PAD_OUTER_X: int
      TABLE_NO_SAVED_SETTINGS: int
      TABLE_PAD_OUTER_X: int
      TABLE_PRECISE_WIDTHS: int
      TABLE_REORDERABLE: int
      TABLE_RESIZABLE: int
      TABLE_ROW_BACKGROUND: int
      TABLE_ROW_HEADERS: int
      TABLE_ROW_NONE: int
      TABLE_SCROLL_X: int
      TABLE_SCROLL_Y: int
      TABLE_SIZING_FIXED_FIT: int
      TABLE_SIZING_FIXED_SAME: int
      TABLE_SIZING_STRETCH_PROP: int
      TABLE_SIZING_STRETCH_SAME: int
      TABLE_SORTABLE: int
      TABLE_SORT_MULTI: int
      TABLE_SORT_TRISTATE: int
      TAB_BAR_AUTO_SELECT_NEW_TABS: int
      TAB_BAR_FITTING_POLICY_DEFAULT: int
      TAB_BAR_FITTING_POLICY_MASK: int
      TAB_BAR_FITTING_POLICY_RESIZE_DOWN: int
      TAB_BAR_FITTING_POLICY_SCROLL: int
      TAB_BAR_NONE: int
      TAB_BAR_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
      TAB_BAR_NO_TAB_LIST_SCROLLING_BUTTONS: int
      TAB_BAR_NO_TOOLTIP: int
      TAB_BAR_REORDERABLE: int
      TAB_BAR_TAB_LIST_POPUP_BUTTON: int
      TAB_ITEM_LEADING: int
      TAB_ITEM_NONE: int
      TAB_ITEM_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
      TAB_ITEM_NO_PUSH_ID: int
      TAB_ITEM_NO_REORDER: int
      TAB_ITEM_NO_TOOLTIP: int
      TAB_ITEM_SET_SELECTED: int
      TAB_ITEM_TRAILING: int
      TAB_ITEM_UNSAVED_DOCUMENT: int
      TREE_NODE_ALLOW_ITEM_OVERLAP: int
      TREE_NODE_BULLET: int
      TREE_NODE_COLLAPSING_HEADER: int
      TREE_NODE_DEFAULT_OPEN: int
      TREE_NODE_FRAMED: int
      TREE_NODE_FRAME_PADDING: int
      TREE_NODE_LEAF: int
      TREE_NODE_NAV_LEFT_JUPS_BACK_HERE: int
      TREE_NODE_NONE: int
      TREE_NODE_NO_AUTO_OPEN_ON_LOG: int
      TREE_NODE_NO_TREE_PUSH_ON_OPEN: int
      TREE_NODE_OPEN_ON_ARROW: int
      TREE_NODE_OPEN_ON_DOUBLE_CLICK: int
      TREE_NODE_SELECTED: int
      TREE_NODE_SPAN_AVAILABLE_WIDTH: int
      TREE_NODE_SPAN_FULL_WIDTH: int
      VIEWPORT_FLAGS_IS_PLATFORM_MONITOR: int
      VIEWPORT_FLAGS_IS_PLATFORM_WINDOW: int
      VIEWPORT_FLAGS_NONE: int
      VIEWPORT_FLAGS_OWNED_BY_APP: int
      WINDOW_ALWAYS_AUTO_RESIZE: int
      WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR: int
      WINDOW_ALWAYS_USE_WINDOW_PADDING: int
      WINDOW_ALWAYS_VERTICAL_SCROLLBAR: int
      WINDOW_HORIZONTAL_SCROLLING_BAR: int
      WINDOW_MENU_BAR: int
      WINDOW_NONE: int
      WINDOW_NO_BACKGROUND: int
      WINDOW_NO_BRING_TO_FRONT_ON_FOCUS: int
      WINDOW_NO_COLLAPSE: int
      WINDOW_NO_DECORATION: int
      WINDOW_NO_FOCUS_ON_APPEARING: int
      WINDOW_NO_INPUTS: int
      WINDOW_NO_MOUSE_INPUTS: int
      WINDOW_NO_MOVE: int
      WINDOW_NO_NAV: int
      WINDOW_NO_NAV_FOCUS: int
      WINDOW_NO_NAV_INPUTS: int
      WINDOW_NO_RESIZE: int
      WINDOW_NO_SAVED_SETTINGS: int
      WINDOW_NO_SCROLLBAR: int
      WINDOW_NO_SCROLL_WITH_MOUSE: int
      WINDOW_NO_TITLE_BAR: int
      WINDOW_UNSAVED_DOCUMENT: int
      _contexts: dict
      _io_clipboard: dict

      @staticmethod
      def _ansifeed_text_ansi(): ...

      @staticmethod
      def _ansifeed_text_ansi_colored(): ...

      @staticmethod
      def _py_colored(variable, r, g, b, a=1.0): ...

      @staticmethod
      def _py_font(font): ...

      @staticmethod
      def _py_index_buffer_index_size(): ...

      @staticmethod
      def _py_istyled(*variables_and_values): ...

      @staticmethod
      def _py_scoped(str_id): ...

      @staticmethod
      def _py_styled(variable, value): ...

      @staticmethod
      def _py_vertex_buffer_vertex_col_offset(): ...

      @staticmethod
      def _py_vertex_buffer_vertex_pos_offset(): ...

      @staticmethod
      def _py_vertex_buffer_vertex_size(): ...

      @staticmethod
      def _py_vertex_buffer_vertex_uv_offset(): ...

      @staticmethod
      def accept_drag_drop_payload(): ...

      @staticmethod
      def align_text_to_frame_padding(): ...

      @staticmethod
      def arrow_button(): ...

      @staticmethod
      def begin(): ...

      @staticmethod
      def begin_child(label, width=0, height=0, border=False, flags=0): ...

      @staticmethod
      def begin_combo(): ...

      @staticmethod
      def begin_drag_drop_source(): ...

      @staticmethod
      def begin_drag_drop_target(): ...

      @staticmethod
      def begin_group(): ...

      @staticmethod
      def begin_list_box(): ...

      @staticmethod
      def begin_main_menu_bar(): ...

      @staticmethod
      def begin_menu(): ...

      @staticmethod
      def begin_menu_bar(): ...

      @staticmethod
      def begin_popup(): ...

      @staticmethod
      def begin_popup_context_item(): ...

      @staticmethod
      def begin_popup_context_void(): ...

      @staticmethod
      def begin_popup_context_window(): ...

      @staticmethod
      def begin_popup_modal(): ...

      @staticmethod
      def begin_tab_bar(): ...

      @staticmethod
      def begin_tab_item(): ...

      @staticmethod
      def begin_table(): ...

      @staticmethod
      def begin_tooltip(): ...

      @staticmethod
      def bullet(): ...

      @staticmethod
      def bullet_text(): ...

      @staticmethod
      def button(): ...

      @staticmethod
      def calc_text_size(): ...

      @staticmethod
      def calculate_item_width(): ...

      @staticmethod
      def capture_mouse_from_app(): ...

      @staticmethod
      def checkbox(): ...

      @staticmethod
      def checkbox_flags(): ...

      @staticmethod
      def close_current_popup(): ...

      @staticmethod
      def collapsing_header(): ...

      @staticmethod
      def color_button(): ...

      @staticmethod
      def color_convert_float4_to_u32(): ...

      @staticmethod
      def color_convert_hsv_to_rgb(): ...

      @staticmethod
      def color_convert_rgb_to_hsv(): ...

      @staticmethod
      def color_convert_u32_to_float4(): ...

      @staticmethod
      def color_edit3(): ...

      @staticmethod
      def color_edit4(): ...

      @staticmethod
      def columns(): ...

      @staticmethod
      def combo(): ...

      @staticmethod
      def contextmanager(func): ...

      @staticmethod
      def create_context(): ...

      @staticmethod
      def destroy_context(): ...

      @staticmethod
      def drag_float(): ...

      @staticmethod
      def drag_float2(): ...

      @staticmethod
      def drag_float3(): ...

      @staticmethod
      def drag_float4(): ...

      @staticmethod
      def drag_float_range2(): ...

      @staticmethod
      def drag_int(): ...

      @staticmethod
      def drag_int2(): ...

      @staticmethod
      def drag_int3(): ...

      @staticmethod
      def drag_int4(): ...

      @staticmethod
      def drag_int_range2(): ...

      @staticmethod
      def drag_scalar(): ...

      @staticmethod
      def drag_scalar_N(): ...

      @staticmethod
      def dummy(): ...

      @staticmethod
      def end(): ...

      @staticmethod
      def end_child(): ...

      @staticmethod
      def end_combo(): ...

      @staticmethod
      def end_drag_drop_source(): ...

      @staticmethod
      def end_drag_drop_target(): ...

      @staticmethod
      def end_frame(): ...

      @staticmethod
      def end_group(): ...

      @staticmethod
      def end_list_box(): ...

      @staticmethod
      def end_main_menu_bar(): ...

      @staticmethod
      def end_menu(): ...

      @staticmethod
      def end_menu_bar(): ...

      @staticmethod
      def end_popup(): ...

      @staticmethod
      def end_tab_bar(): ...

      @staticmethod
      def end_tab_item(): ...

      @staticmethod
      def end_table(): ...

      @staticmethod
      def end_tooltip(): ...

      @staticmethod
      def get_background_draw_list(): ...

      @staticmethod
      def get_clipboard_text(): ...

      @staticmethod
      def get_color_u32(): ...

      @staticmethod
      def get_color_u32_idx(): ...

      @staticmethod
      def get_color_u32_rgba(): ...

      @staticmethod
      def get_column_index(): ...

      @staticmethod
      def get_column_offset(): ...

      @staticmethod
      def get_column_width(): ...

      @staticmethod
      def get_columns_count(): ...

      @staticmethod
      def get_content_region_available(): ...

      @staticmethod
      def get_content_region_available_width(): ...

      @staticmethod
      def get_content_region_max(): ...

      @staticmethod
      def get_current_context(): ...

      @staticmethod
      def get_cursor_pos(): ...

      @staticmethod
      def get_cursor_pos_x(): ...

      @staticmethod
      def get_cursor_pos_y(): ...

      @staticmethod
      def get_cursor_position(): ...

      @staticmethod
      def get_cursor_screen_pos(): ...

      @staticmethod
      def get_cursor_screen_position(): ...

      @staticmethod
      def get_cursor_start_pos(): ...

      @staticmethod
      def get_cursor_start_position(): ...

      @staticmethod
      def get_drag_drop_payload(): ...

      @staticmethod
      def get_draw_data(): ...

      @staticmethod
      def get_font_size(): ...

      @staticmethod
      def get_font_tex_uv_white_pixel(): ...

      @staticmethod
      def get_foreground_draw_list(): ...

      @staticmethod
      def get_frame_height(): ...

      @staticmethod
      def get_frame_height_with_spacing(): ...

      @staticmethod
      def get_io(): ...

      @staticmethod
      def get_item_rect_max(): ...

      @staticmethod
      def get_item_rect_min(): ...

      @staticmethod
      def get_item_rect_size(): ...

      @staticmethod
      def get_key_index(): ...

      @staticmethod
      def get_main_viewport(): ...

      @staticmethod
      def get_mouse_cursor(): ...

      @staticmethod
      def get_mouse_drag_delta(): ...

      @staticmethod
      def get_mouse_pos(): ...

      @staticmethod
      def get_mouse_position(): ...

      @staticmethod
      def get_overlay_draw_list(): ...

      @staticmethod
      def get_scroll_max_x(): ...

      @staticmethod
      def get_scroll_max_y(): ...

      @staticmethod
      def get_scroll_x(): ...

      @staticmethod
      def get_scroll_y(): ...

      @staticmethod
      def get_style(): ...

      @staticmethod
      def get_style_color_name(): ...

      @staticmethod
      def get_style_color_vec_4(): ...

      @staticmethod
      def get_text_line_height(): ...

      @staticmethod
      def get_text_line_height_with_spacing(): ...

      @staticmethod
      def get_time(): ...

      @staticmethod
      def get_tree_node_to_label_spacing(): ...

      @staticmethod
      def get_version(): ...

      @staticmethod
      def get_window_content_region_max(): ...

      @staticmethod
      def get_window_content_region_min(): ...

      @staticmethod
      def get_window_content_region_width(): ...

      @staticmethod
      def get_window_draw_list(): ...

      @staticmethod
      def get_window_height(): ...

      @staticmethod
      def get_window_position(): ...

      @staticmethod
      def get_window_size(): ...

      @staticmethod
      def get_window_width(): ...

      @staticmethod
      def image(): ...

      @staticmethod
      def image_button(): ...

      @staticmethod
      def indent(): ...

      @staticmethod
      def input_double(): ...

      @staticmethod
      def input_float(): ...

      @staticmethod
      def input_float2(): ...

      @staticmethod
      def input_float3(): ...

      @staticmethod
      def input_float4(): ...

      @staticmethod
      def input_int(): ...

      @staticmethod
      def input_int2(): ...

      @staticmethod
      def input_int3(): ...

      @staticmethod
      def input_int4(): ...

      @staticmethod
      def input_scalar(): ...

      @staticmethod
      def input_scalar_N(): ...

      @staticmethod
      def input_text(): ...

      @staticmethod
      def input_text_multiline(): ...

      @staticmethod
      def input_text_with_hint(): ...

      @staticmethod
      def invisible_button(): ...

      @staticmethod
      def is_any_item_active(): ...

      @staticmethod
      def is_any_item_focused(): ...

      @staticmethod
      def is_any_item_hovered(): ...

      @staticmethod
      def is_item_activated(): ...

      @staticmethod
      def is_item_active(): ...

      @staticmethod
      def is_item_clicked(): ...

      @staticmethod
      def is_item_deactivated(): ...

      @staticmethod
      def is_item_deactivated_after_edit(): ...

      @staticmethod
      def is_item_edited(): ...

      @staticmethod
      def is_item_focused(): ...

      @staticmethod
      def is_item_hovered(): ...

      @staticmethod
      def is_item_toggled_open(): ...

      @staticmethod
      def is_item_visible(): ...

      @staticmethod
      def is_key_down(): ...

      @staticmethod
      def is_key_pressed(): ...

      @staticmethod
      def is_mouse_clicked(): ...

      @staticmethod
      def is_mouse_double_clicked(): ...

      @staticmethod
      def is_mouse_down(): ...

      @staticmethod
      def is_mouse_dragging(): ...

      @staticmethod
      def is_mouse_hovering_rect(): ...

      @staticmethod
      def is_mouse_released(): ...

      @staticmethod
      def is_popup_open(): ...

      @staticmethod
      def is_rect_visible(): ...

      @staticmethod
      def is_window_appearing(): ...

      @staticmethod
      def is_window_collapsed(): ...

      @staticmethod
      def is_window_focused(): ...

      @staticmethod
      def is_window_hovered(): ...

      @staticmethod
      def label_text(): ...

      @staticmethod
      def listbox(): ...

      @staticmethod
      def listbox_footer(): ...

      @staticmethod
      def listbox_header(): ...

      @staticmethod
      def load_ini_settings_from_disk(): ...

      @staticmethod
      def load_ini_settings_from_memory(): ...

      @staticmethod
      def menu_item(): ...

      @staticmethod
      def namedtuple(typename, field_names, rename=False, defaults=None, module=None): ...

      @staticmethod
      def new_frame(): ...

      @staticmethod
      def new_line(): ...

      @staticmethod
      def next_column(): ...

      @staticmethod
      def open_popup(): ...

      @staticmethod
      def open_popup_on_item_click(): ...

      @staticmethod
      def plot_histogram(): ...

      @staticmethod
      def plot_lines(): ...

      @staticmethod
      def pop_allow_keyboard_focus(): ...

      @staticmethod
      def pop_button_repeat(): ...

      @staticmethod
      def pop_clip_rect(): ...

      @staticmethod
      def pop_font(): ...

      @staticmethod
      def pop_id(): ...

      @staticmethod
      def pop_item_width(): ...

      @staticmethod
      def pop_style_color(): ...

      @staticmethod
      def pop_style_var(): ...

      @staticmethod
      def pop_text_wrap_pos(): ...

      @staticmethod
      def pop_text_wrap_position(): ...

      @staticmethod
      def progress_bar(): ...

      @staticmethod
      def push_allow_keyboard_focus(): ...

      @staticmethod
      def push_button_repeat(): ...

      @staticmethod
      def push_clip_rect(): ...

      @staticmethod
      def push_font(): ...

      @staticmethod
      def push_id(): ...

      @staticmethod
      def push_item_width(): ...

      @staticmethod
      def push_style_color(): ...

      @staticmethod
      def push_style_var(): ...

      @staticmethod
      def push_text_wrap_pos(): ...

      @staticmethod
      def push_text_wrap_position(): ...

      @staticmethod
      def radio_button(): ...

      @staticmethod
      def render(): ...

      @staticmethod
      def reset_mouse_drag_delta(): ...

      @staticmethod
      def same_line(): ...

      @staticmethod
      def save_ini_settings_to_disk(): ...

      @staticmethod
      def save_ini_settings_to_memory(): ...

      @staticmethod
      def selectable(): ...

      @staticmethod
      def separator(): ...

      @staticmethod
      def set_clipboard_text(): ...

      @staticmethod
      def set_column_offset(): ...

      @staticmethod
      def set_column_width(): ...

      @staticmethod
      def set_current_context(): ...

      @staticmethod
      def set_cursor_pos(): ...

      @staticmethod
      def set_cursor_pos_x(): ...

      @staticmethod
      def set_cursor_pos_y(): ...

      @staticmethod
      def set_cursor_position(): ...

      @staticmethod
      def set_cursor_screen_pos(): ...

      @staticmethod
      def set_cursor_screen_position(): ...

      @staticmethod
      def set_drag_drop_payload(): ...

      @staticmethod
      def set_item_allow_overlap(): ...

      @staticmethod
      def set_item_default_focus(): ...

      @staticmethod
      def set_keyboard_focus_here(): ...

      @staticmethod
      def set_mouse_cursor(): ...

      @staticmethod
      def set_next_item_open(): ...

      @staticmethod
      def set_next_item_width(): ...

      @staticmethod
      def set_next_window_bg_alpha(): ...

      @staticmethod
      def set_next_window_collapsed(): ...

      @staticmethod
      def set_next_window_content_size(): ...

      @staticmethod
      def set_next_window_focus(): ...

      @staticmethod
      def set_next_window_position(): ...

      @staticmethod
      def set_next_window_size(): ...

      @staticmethod
      def set_next_window_size_constraints(): ...

      @staticmethod
      def set_scroll_from_pos_x(): ...

      @staticmethod
      def set_scroll_from_pos_y(): ...

      @staticmethod
      def set_scroll_here_x(): ...

      @staticmethod
      def set_scroll_here_y(): ...

      @staticmethod
      def set_scroll_x(): ...

      @staticmethod
      def set_scroll_y(): ...

      @staticmethod
      def set_tab_item_closed(): ...

      @staticmethod
      def set_tooltip(): ...

      @staticmethod
      def set_window_collapsed(): ...

      @staticmethod
      def set_window_collapsed_labeled(): ...

      @staticmethod
      def set_window_focus(): ...

      @staticmethod
      def set_window_focus_labeled(): ...

      @staticmethod
      def set_window_font_scale(): ...

      @staticmethod
      def set_window_position(): ...

      @staticmethod
      def set_window_position_labeled(): ...

      @staticmethod
      def set_window_size(): ...

      @staticmethod
      def set_window_size_named(): ...

      @staticmethod
      def show_about_window(): ...

      @staticmethod
      def show_demo_window(): ...

      @staticmethod
      def show_font_selector(): ...

      @staticmethod
      def show_metrics_window(): ...

      @staticmethod
      def show_style_editor(): ...

      @staticmethod
      def show_style_selector(): ...

      @staticmethod
      def show_test_window(): ...

      @staticmethod
      def show_user_guide(): ...

      @staticmethod
      def slider_angle(): ...

      @staticmethod
      def slider_float(): ...

      @staticmethod
      def slider_float2(): ...

      @staticmethod
      def slider_float3(): ...

      @staticmethod
      def slider_float4(): ...

      @staticmethod
      def slider_int(): ...

      @staticmethod
      def slider_int2(): ...

      @staticmethod
      def slider_int3(): ...

      @staticmethod
      def slider_int4(): ...

      @staticmethod
      def slider_scalar(): ...

      @staticmethod
      def slider_scalar_N(): ...

      @staticmethod
      def small_button(): ...

      @staticmethod
      def spacing(): ...

      @staticmethod
      def style_colors_classic(): ...

      @staticmethod
      def style_colors_dark(): ...

      @staticmethod
      def style_colors_light(): ...

      @staticmethod
      def tab_item_button(): ...

      @staticmethod
      def table_get_column_count(): ...

      @staticmethod
      def table_get_column_flags(): ...

      @staticmethod
      def table_get_column_index(): ...

      @staticmethod
      def table_get_column_name(): ...

      @staticmethod
      def table_get_row_index(): ...

      @staticmethod
      def table_get_sort_specs(): ...

      @staticmethod
      def table_header(): ...

      @staticmethod
      def table_headers_row(): ...

      @staticmethod
      def table_next_column(): ...

      @staticmethod
      def table_next_row(): ...

      @staticmethod
      def table_set_background_color(): ...

      @staticmethod
      def table_set_column_index(): ...

      @staticmethod
      def table_setup_column(): ...

      @staticmethod
      def table_setup_scroll_freeze(): ...

      @staticmethod
      def text(): ...

      @staticmethod
      def text_colored(): ...

      @staticmethod
      def text_disabled(): ...

      @staticmethod
      def text_unformatted(): ...

      @staticmethod
      def text_wrapped(): ...

      @staticmethod
      def tree_node(): ...

      @staticmethod
      def tree_pop(): ...

      @staticmethod
      def unindent(): ...

      @staticmethod
      def v_slider_float(): ...

      @staticmethod
      def v_slider_int(): ...

      @staticmethod
      def v_slider_scalar(): ...

      class FontConfig: ...

      class GlyphRanges: ...

      class GuiStyle:
        alpha: alpha
        anti_aliased_fill: anti_aliased_fill
        anti_aliased_line_use_tex: anti_aliased_line_use_tex
        anti_aliased_lines: anti_aliased_lines
        button_text_align: button_text_align
        cell_padding: cell_padding
        child_border_size: child_border_size
        child_rounding: child_rounding
        circle_segment_max_error: circle_segment_max_error
        circle_tessellation_max_error: circle_tessellation_max_error
        color_button_position: color_button_position
        colors: colors
        columns_min_spacing: columns_min_spacing
        curve_tessellation_tolerance: curve_tessellation_tolerance
        display_safe_area_padding: display_safe_area_padding
        display_window_padding: display_window_padding
        frame_border_size: frame_border_size
        frame_padding: frame_padding
        frame_rounding: frame_rounding
        grab_min_size: grab_min_size
        grab_rounding: grab_rounding
        indent_spacing: indent_spacing
        item_inner_spacing: item_inner_spacing
        item_spacing: item_spacing
        log_slider_deadzone: log_slider_deadzone
        mouse_cursor_scale: mouse_cursor_scale
        popup_border_size: popup_border_size
        popup_rounding: popup_rounding
        scrollbar_rounding: scrollbar_rounding
        scrollbar_size: scrollbar_size
        selectable_text_align: selectable_text_align
        tab_border_size: tab_border_size
        tab_min_width_for_close_button: tab_min_width_for_close_button
        tab_rounding: tab_rounding
        touch_extra_padding: touch_extra_padding
        window_border_size: window_border_size
        window_menu_button_position: window_menu_button_position
        window_min_size: window_min_size
        window_padding: window_padding
        window_rounding: window_rounding
        window_title_align: window_title_align

        @staticmethod
        def color(): ...

        @staticmethod
        def create(): ...

      class ImGuiError:
        args: args

        @staticmethod
        def add_note(): ...

        @staticmethod
        def with_traceback(): ...

      class Vec2:
        _field_defaults: dict
        _fields: tuple
        x: _tuplegetter
        y: _tuplegetter

        @staticmethod
        def _asdict(self): ...

        @staticmethod
        def _make(iterable): ...

        @staticmethod
        def _replace(self, **kwds): ...

        @staticmethod
        def count(self, value): ...

        @staticmethod
        def index(self, value, start=0, stop=9223372036854775807): ...

      class Vec4:
        _field_defaults: dict
        _fields: tuple
        w: _tuplegetter
        x: _tuplegetter
        y: _tuplegetter
        z: _tuplegetter

        @staticmethod
        def _asdict(self): ...

        @staticmethod
        def _make(iterable): ...

        @staticmethod
        def _replace(self, **kwds): ...

        @staticmethod
        def count(self, value): ...

        @staticmethod
        def index(self, value, start=0, stop=9223372036854775807): ...

      class _BeginEnd:
        expanded: expanded
        opened: opened

      class _BeginEndChild:
        visible: visible

      class _BeginEndCombo:
        opened: opened

      class _BeginEndDragDropSource:
        dragging: dragging

      class _BeginEndDragDropTarget:
        hovered: hovered

      class _BeginEndGroup: ...

      class _BeginEndListBox:
        opened: opened

      class _BeginEndMainMenuBar:
        opened: opened

      class _BeginEndMenu:
        opened: opened

      class _BeginEndMenuBar:
        opened: opened

      class _BeginEndPopup:
        opened: opened

      class _BeginEndPopupModal:
        opened: opened
        visible: visible

      class _BeginEndTabBar:
        opened: opened

      class _BeginEndTabItem:
        opened: opened
        selected: selected

      class _BeginEndTable:
        opened: opened

      class _BeginEndTooltip: ...

      class _Colors: ...

      class _DrawCmd:
        clip_rect: clip_rect
        elem_count: elem_count
        texture_id: texture_id

      class _DrawData:
        cmd_count: cmd_count
        commands_lists: commands_lists
        display_pos: display_pos
        display_size: display_size
        frame_buffer_scale: frame_buffer_scale
        total_idx_count: total_idx_count
        total_vtx_count: total_vtx_count
        valid: valid

        @staticmethod
        def _require_pointer(): ...

        @staticmethod
        def deindex_all_buffers(): ...

        @staticmethod
        def scale_clip_rects(): ...

      class _DrawList:
        cmd_buffer_data: cmd_buffer_data
        cmd_buffer_size: cmd_buffer_size
        commands: commands
        flags: flags
        idx_buffer_data: idx_buffer_data
        idx_buffer_size: idx_buffer_size
        vtx_buffer_data: vtx_buffer_data
        vtx_buffer_size: vtx_buffer_size

        @staticmethod
        def add_bezier_cubic(): ...

        @staticmethod
        def add_bezier_quadratic(): ...

        @staticmethod
        def add_circle(): ...

        @staticmethod
        def add_circle_filled(): ...

        @staticmethod
        def add_image(): ...

        @staticmethod
        def add_image_rounded(): ...

        @staticmethod
        def add_line(): ...

        @staticmethod
        def add_ngon(): ...

        @staticmethod
        def add_ngon_filled(): ...

        @staticmethod
        def add_polyline(): ...

        @staticmethod
        def add_quad(): ...

        @staticmethod
        def add_quad_filled(): ...

        @staticmethod
        def add_rect(): ...

        @staticmethod
        def add_rect_filled(): ...

        @staticmethod
        def add_rect_filled_multicolor(): ...

        @staticmethod
        def add_text(): ...

        @staticmethod
        def add_triangle(): ...

        @staticmethod
        def add_triangle_filled(): ...

        @staticmethod
        def channels_merge(): ...

        @staticmethod
        def channels_set_current(): ...

        @staticmethod
        def channels_split(): ...

        @staticmethod
        def get_clip_rect_max(): ...

        @staticmethod
        def get_clip_rect_min(): ...

        @staticmethod
        def path_arc_to(): ...

        @staticmethod
        def path_arc_to_fast(): ...

        @staticmethod
        def path_clear(): ...

        @staticmethod
        def path_fill_convex(): ...

        @staticmethod
        def path_line_to(): ...

        @staticmethod
        def path_rect(): ...

        @staticmethod
        def path_stroke(): ...

        @staticmethod
        def pop_clip_rect(): ...

        @staticmethod
        def pop_texture_id(): ...

        @staticmethod
        def prim_quad_UV(): ...

        @staticmethod
        def prim_rect(): ...

        @staticmethod
        def prim_rect_UV(): ...

        @staticmethod
        def prim_reserve(): ...

        @staticmethod
        def prim_unreserve(): ...

        @staticmethod
        def prim_vtx(): ...

        @staticmethod
        def prim_write_idx(): ...

        @staticmethod
        def prim_write_vtx(): ...

        @staticmethod
        def push_clip_rect(): ...

        @staticmethod
        def push_clip_rect_full_screen(): ...

        @staticmethod
        def push_texture_id(): ...

      class _Font: ...

      class _FontAtlas:
        texture_desired_width: texture_desired_width
        texture_height: texture_height
        texture_id: texture_id
        texture_width: texture_width

        @staticmethod
        def _require_pointer(): ...

        @staticmethod
        def add_font_default(): ...

        @staticmethod
        def add_font_from_file_ttf(): ...

        @staticmethod
        def clear(): ...

        @staticmethod
        def clear_fonts(): ...

        @staticmethod
        def clear_input_data(): ...

        @staticmethod
        def clear_tex_data(): ...

        @staticmethod
        def get_glyph_ranges_chinese(): ...

        @staticmethod
        def get_glyph_ranges_chinese_full(): ...

        @staticmethod
        def get_glyph_ranges_cyrillic(): ...

        @staticmethod
        def get_glyph_ranges_default(): ...

        @staticmethod
        def get_glyph_ranges_japanese(): ...

        @staticmethod
        def get_glyph_ranges_korean(): ...

        @staticmethod
        def get_glyph_ranges_latin(): ...

        @staticmethod
        def get_glyph_ranges_thai(): ...

        @staticmethod
        def get_glyph_ranges_vietnamese(): ...

        @staticmethod
        def get_tex_data_as_alpha8(): ...

        @staticmethod
        def get_tex_data_as_rgba32(): ...

      class _IO:
        backend_flags: backend_flags
        config_cursor_blink: config_cursor_blink
        config_drag_click_to_input_text: config_drag_click_to_input_text
        config_flags: config_flags
        config_mac_osx_behaviors: config_mac_osx_behaviors
        config_memory_compact_timer: config_memory_compact_timer
        config_windows_move_from_title_bar_only: config_windows_move_from_title_bar_only
        config_windows_resize_from_edges: config_windows_resize_from_edges
        delta_time: delta_time
        display_fb_scale: display_fb_scale
        display_size: display_size
        font_allow_user_scaling: font_allow_user_scaling
        font_global_scale: font_global_scale
        fonts: fonts
        framerate: framerate
        get_clipboard_text_fn: get_clipboard_text_fn
        ini_file_name: ini_file_name
        ini_saving_rate: ini_saving_rate
        key_alt: key_alt
        key_ctrl: key_ctrl
        key_map: key_map
        key_repeat_delay: key_repeat_delay
        key_repeat_rate: key_repeat_rate
        key_shift: key_shift
        key_super: key_super
        keys_down: keys_down
        log_file_name: log_file_name
        metrics_active_allocations: metrics_active_allocations
        metrics_active_windows: metrics_active_windows
        metrics_render_indices: metrics_render_indices
        metrics_render_vertices: metrics_render_vertices
        metrics_render_windows: metrics_render_windows
        mouse_delta: mouse_delta
        mouse_double_click_max_distance: mouse_double_click_max_distance
        mouse_double_click_time: mouse_double_click_time
        mouse_down: mouse_down
        mouse_drag_threshold: mouse_drag_threshold
        mouse_draw_cursor: mouse_draw_cursor
        mouse_pos: mouse_pos
        mouse_wheel: mouse_wheel
        mouse_wheel_horizontal: mouse_wheel_horizontal
        nav_active: nav_active
        nav_inputs: nav_inputs
        nav_visible: nav_visible
        set_clipboard_text_fn: set_clipboard_text_fn
        want_capture_keyboard: want_capture_keyboard
        want_capture_mouse: want_capture_mouse
        want_save_ini_settings: want_save_ini_settings
        want_set_mouse_pos: want_set_mouse_pos
        want_text_input: want_text_input

        @staticmethod
        def add_input_character(): ...

        @staticmethod
        def add_input_character_utf16(): ...

        @staticmethod
        def add_input_characters_utf8(): ...

        @staticmethod
        def clear_input_characters(): ...

      class _ImGuiContext:
        _keepalive_cache: list

      class _ImGuiInputTextCallbackData:
        buffer: buffer
        buffer_dirty: buffer_dirty
        buffer_size: buffer_size
        buffer_text_length: buffer_text_length
        cursor_pos: cursor_pos
        event_char: event_char
        event_flag: event_flag
        event_key: event_key
        flags: flags
        selection_end: selection_end
        selection_start: selection_start
        user_data: user_data

        @staticmethod
        def _require_pointer(): ...

        @staticmethod
        def clear_selection(): ...

        @staticmethod
        def delete_chars(): ...

        @staticmethod
        def has_selection(): ...

        @staticmethod
        def insert_chars(): ...

        @staticmethod
        def select_all(): ...

      class _ImGuiSizeCallbackData:
        current_size: current_size
        desired_size: desired_size
        pos: pos
        user_data: user_data

        @staticmethod
        def _require_pointer(): ...

      class _ImGuiTableColumnSortSpecs:
        column_index: column_index
        column_user_id: column_user_id
        sort_direction: sort_direction
        sort_order: sort_order

        @staticmethod
        def _require_pointer(): ...

      class _ImGuiTableColumnSortSpecs_array:
        @staticmethod
        def _require_pointer(): ...

      class _ImGuiTableSortSpecs:
        specs: specs
        specs_count: specs_count
        specs_dirty: specs_dirty

        @staticmethod
        def _require_pointer(): ...

      class _ImGuiViewport:
        flags: flags
        pos: pos
        size: size
        work_pos: work_pos
        work_size: work_size

        @staticmethod
        def _require_pointer(): ...

        @staticmethod
        def get_center(): ...

        @staticmethod
        def get_work_center(): ...

      class _InputTextSharedBuffer: ...

      class _StaticGlyphRanges: ...

      class _callback_user_info:
        @staticmethod
        def populate(): ...

      class zip_longest: ...

    class extra:
      @staticmethod
      def colored(variable, r, g, b, a=1.0): ...

      @staticmethod
      def font(font): ...

      @staticmethod
      def index_buffer_index_size(): ...

      @staticmethod
      def istyled(*variables_and_values): ...

      @staticmethod
      def scoped(str_id): ...

      @staticmethod
      def styled(variable, value): ...

      @staticmethod
      def text_ansi(): ...

      @staticmethod
      def text_ansi_colored(): ...

      @staticmethod
      def vertex_buffer_vertex_col_offset(): ...

      @staticmethod
      def vertex_buffer_vertex_pos_offset(): ...

      @staticmethod
      def vertex_buffer_vertex_size(): ...

      @staticmethod
      def vertex_buffer_vertex_uv_offset(): ...

      class core:
        ALWAYS: int
        APPEARING: int
        BACKEND_HAS_GAMEPAD: int
        BACKEND_HAS_MOUSE_CURSORS: int
        BACKEND_HAS_SET_MOUSE_POS: int
        BACKEND_NONE: int
        BACKEND_RENDERER_HAS_VTX_OFFSET: int
        BUTTON_MOUSE_BUTTON_LEFT: int
        BUTTON_MOUSE_BUTTON_MIDDLE: int
        BUTTON_MOUSE_BUTTON_RIGHT: int
        BUTTON_NONE: int
        COLOR_BORDER: int
        COLOR_BORDER_SHADOW: int
        COLOR_BUTTON: int
        COLOR_BUTTON_ACTIVE: int
        COLOR_BUTTON_HOVERED: int
        COLOR_CHECK_MARK: int
        COLOR_CHILD_BACKGROUND: int
        COLOR_COUNT: int
        COLOR_DRAG_DROP_TARGET: int
        COLOR_EDIT_ALPHA_BAR: int
        COLOR_EDIT_ALPHA_PREVIEW: int
        COLOR_EDIT_ALPHA_PREVIEW_HALF: int
        COLOR_EDIT_DEFAULT_OPTIONS: int
        COLOR_EDIT_DISPLAY_HEX: int
        COLOR_EDIT_DISPLAY_HSV: int
        COLOR_EDIT_DISPLAY_RGB: int
        COLOR_EDIT_FLOAT: int
        COLOR_EDIT_HDR: int
        COLOR_EDIT_INPUT_HSV: int
        COLOR_EDIT_INPUT_RGB: int
        COLOR_EDIT_NONE: int
        COLOR_EDIT_NO_ALPHA: int
        COLOR_EDIT_NO_BORDER: int
        COLOR_EDIT_NO_DRAG_DROP: int
        COLOR_EDIT_NO_INPUTS: int
        COLOR_EDIT_NO_LABEL: int
        COLOR_EDIT_NO_OPTIONS: int
        COLOR_EDIT_NO_PICKER: int
        COLOR_EDIT_NO_SIDE_PREVIEW: int
        COLOR_EDIT_NO_SMALL_PREVIEW: int
        COLOR_EDIT_NO_TOOLTIP: int
        COLOR_EDIT_PICKER_HUE_BAR: int
        COLOR_EDIT_PICKER_HUE_WHEEL: int
        COLOR_EDIT_UINT8: int
        COLOR_FRAME_BACKGROUND: int
        COLOR_FRAME_BACKGROUND_ACTIVE: int
        COLOR_FRAME_BACKGROUND_HOVERED: int
        COLOR_HEADER: int
        COLOR_HEADER_ACTIVE: int
        COLOR_HEADER_HOVERED: int
        COLOR_MENUBAR_BACKGROUND: int
        COLOR_MODAL_WINDOW_DIM_BACKGROUND: int
        COLOR_NAV_HIGHLIGHT: int
        COLOR_NAV_WINDOWING_DIM_BACKGROUND: int
        COLOR_NAV_WINDOWING_HIGHLIGHT: int
        COLOR_PLOT_HISTOGRAM: int
        COLOR_PLOT_HISTOGRAM_HOVERED: int
        COLOR_PLOT_LINES: int
        COLOR_PLOT_LINES_HOVERED: int
        COLOR_POPUP_BACKGROUND: int
        COLOR_RESIZE_GRIP: int
        COLOR_RESIZE_GRIP_ACTIVE: int
        COLOR_RESIZE_GRIP_HOVERED: int
        COLOR_SCROLLBAR_BACKGROUND: int
        COLOR_SCROLLBAR_GRAB: int
        COLOR_SCROLLBAR_GRAB_ACTIVE: int
        COLOR_SCROLLBAR_GRAB_HOVERED: int
        COLOR_SEPARATOR: int
        COLOR_SEPARATOR_ACTIVE: int
        COLOR_SEPARATOR_HOVERED: int
        COLOR_SLIDER_GRAB: int
        COLOR_SLIDER_GRAB_ACTIVE: int
        COLOR_TAB: int
        COLOR_TABLE_BORDER_LIGHT: int
        COLOR_TABLE_BORDER_STRONG: int
        COLOR_TABLE_HEADER_BACKGROUND: int
        COLOR_TABLE_ROW_BACKGROUND: int
        COLOR_TABLE_ROW_BACKGROUND_ALT: int
        COLOR_TAB_ACTIVE: int
        COLOR_TAB_HOVERED: int
        COLOR_TAB_UNFOCUSED: int
        COLOR_TAB_UNFOCUSED_ACTIVE: int
        COLOR_TEXT: int
        COLOR_TEXT_DISABLED: int
        COLOR_TEXT_SELECTED_BACKGROUND: int
        COLOR_TITLE_BACKGROUND: int
        COLOR_TITLE_BACKGROUND_ACTIVE: int
        COLOR_TITLE_BACKGROUND_COLLAPSED: int
        COLOR_WINDOW_BACKGROUND: int
        COMBO_HEIGHT_LARGE: int
        COMBO_HEIGHT_LARGEST: int
        COMBO_HEIGHT_MASK: int
        COMBO_HEIGHT_REGULAR: int
        COMBO_HEIGHT_SMALL: int
        COMBO_NONE: int
        COMBO_NO_ARROW_BUTTON: int
        COMBO_NO_PREVIEW: int
        COMBO_POPUP_ALIGN_LEFT: int
        CONFIG_IS_RGB: int
        CONFIG_IS_TOUCH_SCREEN: int
        CONFIG_NAV_ENABLE_GAMEPAD: int
        CONFIG_NAV_ENABLE_KEYBOARD: int
        CONFIG_NAV_ENABLE_SET_MOUSE_POS: int
        CONFIG_NAV_NO_CAPTURE_KEYBOARD: int
        CONFIG_NONE: int
        CONFIG_NO_MOUSE: int
        CONFIG_NO_MOUSE_CURSOR_CHANGE: int
        DATA_TYPE_DOUBLE: int
        DATA_TYPE_FLOAT: int
        DATA_TYPE_S16: int
        DATA_TYPE_S32: int
        DATA_TYPE_S64: int
        DATA_TYPE_S8: int
        DATA_TYPE_U16: int
        DATA_TYPE_U32: int
        DATA_TYPE_U64: int
        DATA_TYPE_U8: int
        DIRECTION_DOWN: int
        DIRECTION_LEFT: int
        DIRECTION_NONE: int
        DIRECTION_RIGHT: int
        DIRECTION_UP: int
        DRAG_DROP_ACCEPT_BEFORE_DELIVERY: int
        DRAG_DROP_ACCEPT_NO_DRAW_DEFAULT_RECT: int
        DRAG_DROP_ACCEPT_NO_PREVIEW_TOOLTIP: int
        DRAG_DROP_ACCEPT_PEEK_ONLY: int
        DRAG_DROP_NONE: int
        DRAG_DROP_SOURCE_ALLOW_NULL_ID: int
        DRAG_DROP_SOURCE_AUTO_EXPIRE_PAYLOAD: int
        DRAG_DROP_SOURCE_EXTERN: int
        DRAG_DROP_SOURCE_NO_DISABLE_HOVER: int
        DRAG_DROP_SOURCE_NO_HOLD_TO_OPEN_OTHERS: int
        DRAG_DROP_SOURCE_NO_PREVIEW_TOOLTIP: int
        DRAW_CLOSED: int
        DRAW_CORNER_ALL: int
        DRAW_CORNER_BOTTOM: int
        DRAW_CORNER_BOTTOM_LEFT: int
        DRAW_CORNER_BOTTOM_RIGHT: int
        DRAW_CORNER_LEFT: int
        DRAW_CORNER_NONE: int
        DRAW_CORNER_RIGHT: int
        DRAW_CORNER_TOP: int
        DRAW_CORNER_TOP_LEFT: int
        DRAW_CORNER_TOP_RIGHT: int
        DRAW_LIST_ALLOW_VTX_OFFSET: int
        DRAW_LIST_ANTI_ALIASED_FILL: int
        DRAW_LIST_ANTI_ALIASED_LINES: int
        DRAW_LIST_ANTI_ALIASED_LINES_USE_TEX: int
        DRAW_LIST_NONE: int
        DRAW_NONE: int
        DRAW_ROUND_CORNERS_ALL: int
        DRAW_ROUND_CORNERS_BOTTOM: int
        DRAW_ROUND_CORNERS_BOTTOM_LEFT: int
        DRAW_ROUND_CORNERS_BOTTOM_RIGHT: int
        DRAW_ROUND_CORNERS_LEFT: int
        DRAW_ROUND_CORNERS_NONE: int
        DRAW_ROUND_CORNERS_RIGHT: int
        DRAW_ROUND_CORNERS_TOP: int
        DRAW_ROUND_CORNERS_TOP_LEFT: int
        DRAW_ROUND_CORNERS_TOP_RIGHT: int
        FIRST_USE_EVER: int
        FLOAT_MAX: float
        FLOAT_MIN: float
        FOCUS_ANY_WINDOW: int
        FOCUS_CHILD_WINDOWS: int
        FOCUS_NONE: int
        FOCUS_ROOT_AND_CHILD_WINDOWS: int
        FOCUS_ROOT_WINDOW: int
        FONT_ATLAS_NONE: int
        FONT_ATLAS_NO_BAKED_LINES: int
        FONT_ATLAS_NO_MOUSE_CURSOR: int
        FONT_ATLAS_NO_POWER_OF_TWO_HEIGHT: int
        HOVERED_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM: int
        HOVERED_ALLOW_WHEN_BLOCKED_BY_POPUP: int
        HOVERED_ALLOW_WHEN_DISABLED: int
        HOVERED_ALLOW_WHEN_OVERLAPPED: int
        HOVERED_ANY_WINDOW: int
        HOVERED_CHILD_WINDOWS: int
        HOVERED_NONE: int
        HOVERED_RECT_ONLY: int
        HOVERED_ROOT_AND_CHILD_WINDOWS: int
        HOVERED_ROOT_WINDOW: int
        INPUT_TEXT_ALLOW_TAB_INPUT: int
        INPUT_TEXT_ALWAYS_INSERT_MODE: int
        INPUT_TEXT_ALWAYS_OVERWRITE: int
        INPUT_TEXT_AUTO_SELECT_ALL: int
        INPUT_TEXT_CALLBACK_ALWAYS: int
        INPUT_TEXT_CALLBACK_CHAR_FILTER: int
        INPUT_TEXT_CALLBACK_COMPLETION: int
        INPUT_TEXT_CALLBACK_EDIT: int
        INPUT_TEXT_CALLBACK_HISTORY: int
        INPUT_TEXT_CALLBACK_RESIZE: int
        INPUT_TEXT_CHARS_DECIMAL: int
        INPUT_TEXT_CHARS_HEXADECIMAL: int
        INPUT_TEXT_CHARS_NO_BLANK: int
        INPUT_TEXT_CHARS_SCIENTIFIC: int
        INPUT_TEXT_CHARS_UPPERCASE: int
        INPUT_TEXT_CTRL_ENTER_FOR_NEW_LINE: int
        INPUT_TEXT_ENTER_RETURNS_TRUE: int
        INPUT_TEXT_NONE: int
        INPUT_TEXT_NO_HORIZONTAL_SCROLL: int
        INPUT_TEXT_NO_UNDO_REDO: int
        INPUT_TEXT_PASSWORD: int
        INPUT_TEXT_READ_ONLY: int
        KEY_A: int
        KEY_BACKSPACE: int
        KEY_C: int
        KEY_DELETE: int
        KEY_DOWN_ARROW: int
        KEY_END: int
        KEY_ENTER: int
        KEY_ESCAPE: int
        KEY_HOME: int
        KEY_INSERT: int
        KEY_LEFT_ARROW: int
        KEY_MOD_ALT: int
        KEY_MOD_CTRL: int
        KEY_MOD_NONE: int
        KEY_MOD_SHIFT: int
        KEY_MOD_SUPER: int
        KEY_PAD_ENTER: int
        KEY_PAGE_DOWN: int
        KEY_PAGE_UP: int
        KEY_RIGHT_ARROW: int
        KEY_SPACE: int
        KEY_TAB: int
        KEY_UP_ARROW: int
        KEY_V: int
        KEY_X: int
        KEY_Y: int
        KEY_Z: int
        MOUSE_BUTTON_LEFT: int
        MOUSE_BUTTON_MIDDLE: int
        MOUSE_BUTTON_RIGHT: int
        MOUSE_CURSOR_ARROW: int
        MOUSE_CURSOR_HAND: int
        MOUSE_CURSOR_NONE: int
        MOUSE_CURSOR_NOT_ALLOWED: int
        MOUSE_CURSOR_RESIZE_ALL: int
        MOUSE_CURSOR_RESIZE_EW: int
        MOUSE_CURSOR_RESIZE_NESW: int
        MOUSE_CURSOR_RESIZE_NS: int
        MOUSE_CURSOR_RESIZE_NWSE: int
        MOUSE_CURSOR_TEXT_INPUT: int
        NAV_INPUT_ACTIVATE: int
        NAV_INPUT_CANCEL: int
        NAV_INPUT_COUNT: int
        NAV_INPUT_DPAD_DOWN: int
        NAV_INPUT_DPAD_LEFT: int
        NAV_INPUT_DPAD_RIGHT: int
        NAV_INPUT_DPAD_UP: int
        NAV_INPUT_FOCUS_NEXT: int
        NAV_INPUT_FOCUS_PREV: int
        NAV_INPUT_INPUT: int
        NAV_INPUT_L_STICK_DOWN: int
        NAV_INPUT_L_STICK_LEFT: int
        NAV_INPUT_L_STICK_RIGHT: int
        NAV_INPUT_L_STICK_UP: int
        NAV_INPUT_MENU: int
        NAV_INPUT_TWEAK_FAST: int
        NAV_INPUT_TWEAK_SLOW: int
        NONE: int
        ONCE: int
        POPUP_ANY_POPUP: int
        POPUP_ANY_POPUP_ID: int
        POPUP_ANY_POPUP_LEVEL: int
        POPUP_MOUSE_BUTTON_DEFAULT: int
        POPUP_MOUSE_BUTTON_LEFT: int
        POPUP_MOUSE_BUTTON_MASK: int
        POPUP_MOUSE_BUTTON_MIDDLE: int
        POPUP_MOUSE_BUTTON_RIGHT: int
        POPUP_NONE: int
        POPUP_NO_OPEN_OVER_EXISTING_POPUP: int
        POPUP_NO_OPEN_OVER_ITEMS: int
        SELECTABLE_ALLOW_DOUBLE_CLICK: int
        SELECTABLE_ALLOW_ITEM_OVERLAP: int
        SELECTABLE_DISABLED: int
        SELECTABLE_DONT_CLOSE_POPUPS: int
        SELECTABLE_NONE: int
        SELECTABLE_SPAN_ALL_COLUMNS: int
        SLIDER_FLAGS_ALWAYS_CLAMP: int
        SLIDER_FLAGS_LOGARITHMIC: int
        SLIDER_FLAGS_NONE: int
        SLIDER_FLAGS_NO_INPUT: int
        SLIDER_FLAGS_NO_ROUND_TO_FORMAT: int
        SORT_DIRECTION_ASCENDING: int
        SORT_DIRECTION_DESCENDING: int
        SORT_DIRECTION_NONE: int
        STYLE_ALPHA: int
        STYLE_BUTTON_TEXT_ALIGN: int
        STYLE_CELL_PADDING: int
        STYLE_CHILD_BORDERSIZE: int
        STYLE_CHILD_ROUNDING: int
        STYLE_FRAME_BORDERSIZE: int
        STYLE_FRAME_PADDING: int
        STYLE_FRAME_ROUNDING: int
        STYLE_GRAB_MIN_SIZE: int
        STYLE_GRAB_ROUNDING: int
        STYLE_INDENT_SPACING: int
        STYLE_ITEM_INNER_SPACING: int
        STYLE_ITEM_SPACING: int
        STYLE_POPUP_BORDERSIZE: int
        STYLE_POPUP_ROUNDING: int
        STYLE_SCROLLBAR_ROUNDING: int
        STYLE_SCROLLBAR_SIZE: int
        STYLE_SELECTABLE_TEXT_ALIGN: int
        STYLE_TAB_ROUNDING: int
        STYLE_WINDOW_BORDERSIZE: int
        STYLE_WINDOW_MIN_SIZE: int
        STYLE_WINDOW_PADDING: int
        STYLE_WINDOW_ROUNDING: int
        STYLE_WINDOW_TITLE_ALIGN: int
        TABLE_BACKGROUND_TARGET_CELL_BG: int
        TABLE_BACKGROUND_TARGET_NONE: int
        TABLE_BACKGROUND_TARGET_ROW_BG0: int
        TABLE_BACKGROUND_TARGET_ROW_BG1: int
        TABLE_BORDERS: int
        TABLE_BORDERS_HORIZONTAL: int
        TABLE_BORDERS_INNER: int
        TABLE_BORDERS_INNER_HORIZONTAL: int
        TABLE_BORDERS_INNER_VERTICAL: int
        TABLE_BORDERS_OUTER: int
        TABLE_BORDERS_OUTER_HORIZONTAL: int
        TABLE_BORDERS_OUTER_VERTICAL: int
        TABLE_BORDERS_VERTICAL: int
        TABLE_COLUMN_DEFAULT_HIDE: int
        TABLE_COLUMN_DEFAULT_SORT: int
        TABLE_COLUMN_INDENT_DISABLE: int
        TABLE_COLUMN_INDENT_ENABLE: int
        TABLE_COLUMN_IS_ENABLED: int
        TABLE_COLUMN_IS_HOVERED: int
        TABLE_COLUMN_IS_SORTED: int
        TABLE_COLUMN_IS_VISIBLE: int
        TABLE_COLUMN_NONE: int
        TABLE_COLUMN_NO_CLIP: int
        TABLE_COLUMN_NO_HEADER_WIDTH: int
        TABLE_COLUMN_NO_HIDE: int
        TABLE_COLUMN_NO_REORDER: int
        TABLE_COLUMN_NO_RESIZE: int
        TABLE_COLUMN_NO_SORT: int
        TABLE_COLUMN_NO_SORT_ASCENDING: int
        TABLE_COLUMN_NO_SORT_DESCENDING: int
        TABLE_COLUMN_PREFER_SORT_ASCENDING: int
        TABLE_COLUMN_PREFER_SORT_DESCENDING: int
        TABLE_COLUMN_WIDTH_FIXED: int
        TABLE_COLUMN_WIDTH_STRETCH: int
        TABLE_CONTEXT_MENU_IN_BODY: int
        TABLE_HIDEABLE: int
        TABLE_NONE: int
        TABLE_NO_BORDERS_IN_BODY: int
        TABLE_NO_BORDERS_IN_BODY_UTIL_RESIZE: int
        TABLE_NO_CLIP: int
        TABLE_NO_HOST_EXTEND_X: int
        TABLE_NO_HOST_EXTEND_Y: int
        TABLE_NO_KEEP_COLUMNS_VISIBLE: int
        TABLE_NO_PAD_INNER_X: int
        TABLE_NO_PAD_OUTER_X: int
        TABLE_NO_SAVED_SETTINGS: int
        TABLE_PAD_OUTER_X: int
        TABLE_PRECISE_WIDTHS: int
        TABLE_REORDERABLE: int
        TABLE_RESIZABLE: int
        TABLE_ROW_BACKGROUND: int
        TABLE_ROW_HEADERS: int
        TABLE_ROW_NONE: int
        TABLE_SCROLL_X: int
        TABLE_SCROLL_Y: int
        TABLE_SIZING_FIXED_FIT: int
        TABLE_SIZING_FIXED_SAME: int
        TABLE_SIZING_STRETCH_PROP: int
        TABLE_SIZING_STRETCH_SAME: int
        TABLE_SORTABLE: int
        TABLE_SORT_MULTI: int
        TABLE_SORT_TRISTATE: int
        TAB_BAR_AUTO_SELECT_NEW_TABS: int
        TAB_BAR_FITTING_POLICY_DEFAULT: int
        TAB_BAR_FITTING_POLICY_MASK: int
        TAB_BAR_FITTING_POLICY_RESIZE_DOWN: int
        TAB_BAR_FITTING_POLICY_SCROLL: int
        TAB_BAR_NONE: int
        TAB_BAR_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
        TAB_BAR_NO_TAB_LIST_SCROLLING_BUTTONS: int
        TAB_BAR_NO_TOOLTIP: int
        TAB_BAR_REORDERABLE: int
        TAB_BAR_TAB_LIST_POPUP_BUTTON: int
        TAB_ITEM_LEADING: int
        TAB_ITEM_NONE: int
        TAB_ITEM_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: int
        TAB_ITEM_NO_PUSH_ID: int
        TAB_ITEM_NO_REORDER: int
        TAB_ITEM_NO_TOOLTIP: int
        TAB_ITEM_SET_SELECTED: int
        TAB_ITEM_TRAILING: int
        TAB_ITEM_UNSAVED_DOCUMENT: int
        TREE_NODE_ALLOW_ITEM_OVERLAP: int
        TREE_NODE_BULLET: int
        TREE_NODE_COLLAPSING_HEADER: int
        TREE_NODE_DEFAULT_OPEN: int
        TREE_NODE_FRAMED: int
        TREE_NODE_FRAME_PADDING: int
        TREE_NODE_LEAF: int
        TREE_NODE_NAV_LEFT_JUPS_BACK_HERE: int
        TREE_NODE_NONE: int
        TREE_NODE_NO_AUTO_OPEN_ON_LOG: int
        TREE_NODE_NO_TREE_PUSH_ON_OPEN: int
        TREE_NODE_OPEN_ON_ARROW: int
        TREE_NODE_OPEN_ON_DOUBLE_CLICK: int
        TREE_NODE_SELECTED: int
        TREE_NODE_SPAN_AVAILABLE_WIDTH: int
        TREE_NODE_SPAN_FULL_WIDTH: int
        VIEWPORT_FLAGS_IS_PLATFORM_MONITOR: int
        VIEWPORT_FLAGS_IS_PLATFORM_WINDOW: int
        VIEWPORT_FLAGS_NONE: int
        VIEWPORT_FLAGS_OWNED_BY_APP: int
        WINDOW_ALWAYS_AUTO_RESIZE: int
        WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR: int
        WINDOW_ALWAYS_USE_WINDOW_PADDING: int
        WINDOW_ALWAYS_VERTICAL_SCROLLBAR: int
        WINDOW_HORIZONTAL_SCROLLING_BAR: int
        WINDOW_MENU_BAR: int
        WINDOW_NONE: int
        WINDOW_NO_BACKGROUND: int
        WINDOW_NO_BRING_TO_FRONT_ON_FOCUS: int
        WINDOW_NO_COLLAPSE: int
        WINDOW_NO_DECORATION: int
        WINDOW_NO_FOCUS_ON_APPEARING: int
        WINDOW_NO_INPUTS: int
        WINDOW_NO_MOUSE_INPUTS: int
        WINDOW_NO_MOVE: int
        WINDOW_NO_NAV: int
        WINDOW_NO_NAV_FOCUS: int
        WINDOW_NO_NAV_INPUTS: int
        WINDOW_NO_RESIZE: int
        WINDOW_NO_SAVED_SETTINGS: int
        WINDOW_NO_SCROLLBAR: int
        WINDOW_NO_SCROLL_WITH_MOUSE: int
        WINDOW_NO_TITLE_BAR: int
        WINDOW_UNSAVED_DOCUMENT: int
        _contexts: dict
        _io_clipboard: dict

        @staticmethod
        def _ansifeed_text_ansi(): ...

        @staticmethod
        def _ansifeed_text_ansi_colored(): ...

        @staticmethod
        def _py_colored(variable, r, g, b, a=1.0): ...

        @staticmethod
        def _py_font(font): ...

        @staticmethod
        def _py_index_buffer_index_size(): ...

        @staticmethod
        def _py_istyled(*variables_and_values): ...

        @staticmethod
        def _py_scoped(str_id): ...

        @staticmethod
        def _py_styled(variable, value): ...

        @staticmethod
        def _py_vertex_buffer_vertex_col_offset(): ...

        @staticmethod
        def _py_vertex_buffer_vertex_pos_offset(): ...

        @staticmethod
        def _py_vertex_buffer_vertex_size(): ...

        @staticmethod
        def _py_vertex_buffer_vertex_uv_offset(): ...

        @staticmethod
        def accept_drag_drop_payload(): ...

        @staticmethod
        def align_text_to_frame_padding(): ...

        @staticmethod
        def arrow_button(): ...

        @staticmethod
        def begin(): ...

        @staticmethod
        def begin_child(label, width=0, height=0, border=False, flags=0): ...

        @staticmethod
        def begin_combo(): ...

        @staticmethod
        def begin_drag_drop_source(): ...

        @staticmethod
        def begin_drag_drop_target(): ...

        @staticmethod
        def begin_group(): ...

        @staticmethod
        def begin_list_box(): ...

        @staticmethod
        def begin_main_menu_bar(): ...

        @staticmethod
        def begin_menu(): ...

        @staticmethod
        def begin_menu_bar(): ...

        @staticmethod
        def begin_popup(): ...

        @staticmethod
        def begin_popup_context_item(): ...

        @staticmethod
        def begin_popup_context_void(): ...

        @staticmethod
        def begin_popup_context_window(): ...

        @staticmethod
        def begin_popup_modal(): ...

        @staticmethod
        def begin_tab_bar(): ...

        @staticmethod
        def begin_tab_item(): ...

        @staticmethod
        def begin_table(): ...

        @staticmethod
        def begin_tooltip(): ...

        @staticmethod
        def bullet(): ...

        @staticmethod
        def bullet_text(): ...

        @staticmethod
        def button(): ...

        @staticmethod
        def calc_text_size(): ...

        @staticmethod
        def calculate_item_width(): ...

        @staticmethod
        def capture_mouse_from_app(): ...

        @staticmethod
        def checkbox(): ...

        @staticmethod
        def checkbox_flags(): ...

        @staticmethod
        def close_current_popup(): ...

        @staticmethod
        def collapsing_header(): ...

        @staticmethod
        def color_button(): ...

        @staticmethod
        def color_convert_float4_to_u32(): ...

        @staticmethod
        def color_convert_hsv_to_rgb(): ...

        @staticmethod
        def color_convert_rgb_to_hsv(): ...

        @staticmethod
        def color_convert_u32_to_float4(): ...

        @staticmethod
        def color_edit3(): ...

        @staticmethod
        def color_edit4(): ...

        @staticmethod
        def columns(): ...

        @staticmethod
        def combo(): ...

        @staticmethod
        def contextmanager(func): ...

        @staticmethod
        def create_context(): ...

        @staticmethod
        def destroy_context(): ...

        @staticmethod
        def drag_float(): ...

        @staticmethod
        def drag_float2(): ...

        @staticmethod
        def drag_float3(): ...

        @staticmethod
        def drag_float4(): ...

        @staticmethod
        def drag_float_range2(): ...

        @staticmethod
        def drag_int(): ...

        @staticmethod
        def drag_int2(): ...

        @staticmethod
        def drag_int3(): ...

        @staticmethod
        def drag_int4(): ...

        @staticmethod
        def drag_int_range2(): ...

        @staticmethod
        def drag_scalar(): ...

        @staticmethod
        def drag_scalar_N(): ...

        @staticmethod
        def dummy(): ...

        @staticmethod
        def end(): ...

        @staticmethod
        def end_child(): ...

        @staticmethod
        def end_combo(): ...

        @staticmethod
        def end_drag_drop_source(): ...

        @staticmethod
        def end_drag_drop_target(): ...

        @staticmethod
        def end_frame(): ...

        @staticmethod
        def end_group(): ...

        @staticmethod
        def end_list_box(): ...

        @staticmethod
        def end_main_menu_bar(): ...

        @staticmethod
        def end_menu(): ...

        @staticmethod
        def end_menu_bar(): ...

        @staticmethod
        def end_popup(): ...

        @staticmethod
        def end_tab_bar(): ...

        @staticmethod
        def end_tab_item(): ...

        @staticmethod
        def end_table(): ...

        @staticmethod
        def end_tooltip(): ...

        @staticmethod
        def get_background_draw_list(): ...

        @staticmethod
        def get_clipboard_text(): ...

        @staticmethod
        def get_color_u32(): ...

        @staticmethod
        def get_color_u32_idx(): ...

        @staticmethod
        def get_color_u32_rgba(): ...

        @staticmethod
        def get_column_index(): ...

        @staticmethod
        def get_column_offset(): ...

        @staticmethod
        def get_column_width(): ...

        @staticmethod
        def get_columns_count(): ...

        @staticmethod
        def get_content_region_available(): ...

        @staticmethod
        def get_content_region_available_width(): ...

        @staticmethod
        def get_content_region_max(): ...

        @staticmethod
        def get_current_context(): ...

        @staticmethod
        def get_cursor_pos(): ...

        @staticmethod
        def get_cursor_pos_x(): ...

        @staticmethod
        def get_cursor_pos_y(): ...

        @staticmethod
        def get_cursor_position(): ...

        @staticmethod
        def get_cursor_screen_pos(): ...

        @staticmethod
        def get_cursor_screen_position(): ...

        @staticmethod
        def get_cursor_start_pos(): ...

        @staticmethod
        def get_cursor_start_position(): ...

        @staticmethod
        def get_drag_drop_payload(): ...

        @staticmethod
        def get_draw_data(): ...

        @staticmethod
        def get_font_size(): ...

        @staticmethod
        def get_font_tex_uv_white_pixel(): ...

        @staticmethod
        def get_foreground_draw_list(): ...

        @staticmethod
        def get_frame_height(): ...

        @staticmethod
        def get_frame_height_with_spacing(): ...

        @staticmethod
        def get_io(): ...

        @staticmethod
        def get_item_rect_max(): ...

        @staticmethod
        def get_item_rect_min(): ...

        @staticmethod
        def get_item_rect_size(): ...

        @staticmethod
        def get_key_index(): ...

        @staticmethod
        def get_main_viewport(): ...

        @staticmethod
        def get_mouse_cursor(): ...

        @staticmethod
        def get_mouse_drag_delta(): ...

        @staticmethod
        def get_mouse_pos(): ...

        @staticmethod
        def get_mouse_position(): ...

        @staticmethod
        def get_overlay_draw_list(): ...

        @staticmethod
        def get_scroll_max_x(): ...

        @staticmethod
        def get_scroll_max_y(): ...

        @staticmethod
        def get_scroll_x(): ...

        @staticmethod
        def get_scroll_y(): ...

        @staticmethod
        def get_style(): ...

        @staticmethod
        def get_style_color_name(): ...

        @staticmethod
        def get_style_color_vec_4(): ...

        @staticmethod
        def get_text_line_height(): ...

        @staticmethod
        def get_text_line_height_with_spacing(): ...

        @staticmethod
        def get_time(): ...

        @staticmethod
        def get_tree_node_to_label_spacing(): ...

        @staticmethod
        def get_version(): ...

        @staticmethod
        def get_window_content_region_max(): ...

        @staticmethod
        def get_window_content_region_min(): ...

        @staticmethod
        def get_window_content_region_width(): ...

        @staticmethod
        def get_window_draw_list(): ...

        @staticmethod
        def get_window_height(): ...

        @staticmethod
        def get_window_position(): ...

        @staticmethod
        def get_window_size(): ...

        @staticmethod
        def get_window_width(): ...

        @staticmethod
        def image(): ...

        @staticmethod
        def image_button(): ...

        @staticmethod
        def indent(): ...

        @staticmethod
        def input_double(): ...

        @staticmethod
        def input_float(): ...

        @staticmethod
        def input_float2(): ...

        @staticmethod
        def input_float3(): ...

        @staticmethod
        def input_float4(): ...

        @staticmethod
        def input_int(): ...

        @staticmethod
        def input_int2(): ...

        @staticmethod
        def input_int3(): ...

        @staticmethod
        def input_int4(): ...

        @staticmethod
        def input_scalar(): ...

        @staticmethod
        def input_scalar_N(): ...

        @staticmethod
        def input_text(): ...

        @staticmethod
        def input_text_multiline(): ...

        @staticmethod
        def input_text_with_hint(): ...

        @staticmethod
        def invisible_button(): ...

        @staticmethod
        def is_any_item_active(): ...

        @staticmethod
        def is_any_item_focused(): ...

        @staticmethod
        def is_any_item_hovered(): ...

        @staticmethod
        def is_item_activated(): ...

        @staticmethod
        def is_item_active(): ...

        @staticmethod
        def is_item_clicked(): ...

        @staticmethod
        def is_item_deactivated(): ...

        @staticmethod
        def is_item_deactivated_after_edit(): ...

        @staticmethod
        def is_item_edited(): ...

        @staticmethod
        def is_item_focused(): ...

        @staticmethod
        def is_item_hovered(): ...

        @staticmethod
        def is_item_toggled_open(): ...

        @staticmethod
        def is_item_visible(): ...

        @staticmethod
        def is_key_down(): ...

        @staticmethod
        def is_key_pressed(): ...

        @staticmethod
        def is_mouse_clicked(): ...

        @staticmethod
        def is_mouse_double_clicked(): ...

        @staticmethod
        def is_mouse_down(): ...

        @staticmethod
        def is_mouse_dragging(): ...

        @staticmethod
        def is_mouse_hovering_rect(): ...

        @staticmethod
        def is_mouse_released(): ...

        @staticmethod
        def is_popup_open(): ...

        @staticmethod
        def is_rect_visible(): ...

        @staticmethod
        def is_window_appearing(): ...

        @staticmethod
        def is_window_collapsed(): ...

        @staticmethod
        def is_window_focused(): ...

        @staticmethod
        def is_window_hovered(): ...

        @staticmethod
        def label_text(): ...

        @staticmethod
        def listbox(): ...

        @staticmethod
        def listbox_footer(): ...

        @staticmethod
        def listbox_header(): ...

        @staticmethod
        def load_ini_settings_from_disk(): ...

        @staticmethod
        def load_ini_settings_from_memory(): ...

        @staticmethod
        def menu_item(): ...

        @staticmethod
        def namedtuple(typename, field_names, rename=False, defaults=None, module=None): ...

        @staticmethod
        def new_frame(): ...

        @staticmethod
        def new_line(): ...

        @staticmethod
        def next_column(): ...

        @staticmethod
        def open_popup(): ...

        @staticmethod
        def open_popup_on_item_click(): ...

        @staticmethod
        def plot_histogram(): ...

        @staticmethod
        def plot_lines(): ...

        @staticmethod
        def pop_allow_keyboard_focus(): ...

        @staticmethod
        def pop_button_repeat(): ...

        @staticmethod
        def pop_clip_rect(): ...

        @staticmethod
        def pop_font(): ...

        @staticmethod
        def pop_id(): ...

        @staticmethod
        def pop_item_width(): ...

        @staticmethod
        def pop_style_color(): ...

        @staticmethod
        def pop_style_var(): ...

        @staticmethod
        def pop_text_wrap_pos(): ...

        @staticmethod
        def pop_text_wrap_position(): ...

        @staticmethod
        def progress_bar(): ...

        @staticmethod
        def push_allow_keyboard_focus(): ...

        @staticmethod
        def push_button_repeat(): ...

        @staticmethod
        def push_clip_rect(): ...

        @staticmethod
        def push_font(): ...

        @staticmethod
        def push_id(): ...

        @staticmethod
        def push_item_width(): ...

        @staticmethod
        def push_style_color(): ...

        @staticmethod
        def push_style_var(): ...

        @staticmethod
        def push_text_wrap_pos(): ...

        @staticmethod
        def push_text_wrap_position(): ...

        @staticmethod
        def radio_button(): ...

        @staticmethod
        def render(): ...

        @staticmethod
        def reset_mouse_drag_delta(): ...

        @staticmethod
        def same_line(): ...

        @staticmethod
        def save_ini_settings_to_disk(): ...

        @staticmethod
        def save_ini_settings_to_memory(): ...

        @staticmethod
        def selectable(): ...

        @staticmethod
        def separator(): ...

        @staticmethod
        def set_clipboard_text(): ...

        @staticmethod
        def set_column_offset(): ...

        @staticmethod
        def set_column_width(): ...

        @staticmethod
        def set_current_context(): ...

        @staticmethod
        def set_cursor_pos(): ...

        @staticmethod
        def set_cursor_pos_x(): ...

        @staticmethod
        def set_cursor_pos_y(): ...

        @staticmethod
        def set_cursor_position(): ...

        @staticmethod
        def set_cursor_screen_pos(): ...

        @staticmethod
        def set_cursor_screen_position(): ...

        @staticmethod
        def set_drag_drop_payload(): ...

        @staticmethod
        def set_item_allow_overlap(): ...

        @staticmethod
        def set_item_default_focus(): ...

        @staticmethod
        def set_keyboard_focus_here(): ...

        @staticmethod
        def set_mouse_cursor(): ...

        @staticmethod
        def set_next_item_open(): ...

        @staticmethod
        def set_next_item_width(): ...

        @staticmethod
        def set_next_window_bg_alpha(): ...

        @staticmethod
        def set_next_window_collapsed(): ...

        @staticmethod
        def set_next_window_content_size(): ...

        @staticmethod
        def set_next_window_focus(): ...

        @staticmethod
        def set_next_window_position(): ...

        @staticmethod
        def set_next_window_size(): ...

        @staticmethod
        def set_next_window_size_constraints(): ...

        @staticmethod
        def set_scroll_from_pos_x(): ...

        @staticmethod
        def set_scroll_from_pos_y(): ...

        @staticmethod
        def set_scroll_here_x(): ...

        @staticmethod
        def set_scroll_here_y(): ...

        @staticmethod
        def set_scroll_x(): ...

        @staticmethod
        def set_scroll_y(): ...

        @staticmethod
        def set_tab_item_closed(): ...

        @staticmethod
        def set_tooltip(): ...

        @staticmethod
        def set_window_collapsed(): ...

        @staticmethod
        def set_window_collapsed_labeled(): ...

        @staticmethod
        def set_window_focus(): ...

        @staticmethod
        def set_window_focus_labeled(): ...

        @staticmethod
        def set_window_font_scale(): ...

        @staticmethod
        def set_window_position(): ...

        @staticmethod
        def set_window_position_labeled(): ...

        @staticmethod
        def set_window_size(): ...

        @staticmethod
        def set_window_size_named(): ...

        @staticmethod
        def show_about_window(): ...

        @staticmethod
        def show_demo_window(): ...

        @staticmethod
        def show_font_selector(): ...

        @staticmethod
        def show_metrics_window(): ...

        @staticmethod
        def show_style_editor(): ...

        @staticmethod
        def show_style_selector(): ...

        @staticmethod
        def show_test_window(): ...

        @staticmethod
        def show_user_guide(): ...

        @staticmethod
        def slider_angle(): ...

        @staticmethod
        def slider_float(): ...

        @staticmethod
        def slider_float2(): ...

        @staticmethod
        def slider_float3(): ...

        @staticmethod
        def slider_float4(): ...

        @staticmethod
        def slider_int(): ...

        @staticmethod
        def slider_int2(): ...

        @staticmethod
        def slider_int3(): ...

        @staticmethod
        def slider_int4(): ...

        @staticmethod
        def slider_scalar(): ...

        @staticmethod
        def slider_scalar_N(): ...

        @staticmethod
        def small_button(): ...

        @staticmethod
        def spacing(): ...

        @staticmethod
        def style_colors_classic(): ...

        @staticmethod
        def style_colors_dark(): ...

        @staticmethod
        def style_colors_light(): ...

        @staticmethod
        def tab_item_button(): ...

        @staticmethod
        def table_get_column_count(): ...

        @staticmethod
        def table_get_column_flags(): ...

        @staticmethod
        def table_get_column_index(): ...

        @staticmethod
        def table_get_column_name(): ...

        @staticmethod
        def table_get_row_index(): ...

        @staticmethod
        def table_get_sort_specs(): ...

        @staticmethod
        def table_header(): ...

        @staticmethod
        def table_headers_row(): ...

        @staticmethod
        def table_next_column(): ...

        @staticmethod
        def table_next_row(): ...

        @staticmethod
        def table_set_background_color(): ...

        @staticmethod
        def table_set_column_index(): ...

        @staticmethod
        def table_setup_column(): ...

        @staticmethod
        def table_setup_scroll_freeze(): ...

        @staticmethod
        def text(): ...

        @staticmethod
        def text_colored(): ...

        @staticmethod
        def text_disabled(): ...

        @staticmethod
        def text_unformatted(): ...

        @staticmethod
        def text_wrapped(): ...

        @staticmethod
        def tree_node(): ...

        @staticmethod
        def tree_pop(): ...

        @staticmethod
        def unindent(): ...

        @staticmethod
        def v_slider_float(): ...

        @staticmethod
        def v_slider_int(): ...

        @staticmethod
        def v_slider_scalar(): ...

        class FontConfig: ...

        class GlyphRanges: ...

        class GuiStyle:
          alpha: alpha
          anti_aliased_fill: anti_aliased_fill
          anti_aliased_line_use_tex: anti_aliased_line_use_tex
          anti_aliased_lines: anti_aliased_lines
          button_text_align: button_text_align
          cell_padding: cell_padding
          child_border_size: child_border_size
          child_rounding: child_rounding
          circle_segment_max_error: circle_segment_max_error
          circle_tessellation_max_error: circle_tessellation_max_error
          color_button_position: color_button_position
          colors: colors
          columns_min_spacing: columns_min_spacing
          curve_tessellation_tolerance: curve_tessellation_tolerance
          display_safe_area_padding: display_safe_area_padding
          display_window_padding: display_window_padding
          frame_border_size: frame_border_size
          frame_padding: frame_padding
          frame_rounding: frame_rounding
          grab_min_size: grab_min_size
          grab_rounding: grab_rounding
          indent_spacing: indent_spacing
          item_inner_spacing: item_inner_spacing
          item_spacing: item_spacing
          log_slider_deadzone: log_slider_deadzone
          mouse_cursor_scale: mouse_cursor_scale
          popup_border_size: popup_border_size
          popup_rounding: popup_rounding
          scrollbar_rounding: scrollbar_rounding
          scrollbar_size: scrollbar_size
          selectable_text_align: selectable_text_align
          tab_border_size: tab_border_size
          tab_min_width_for_close_button: tab_min_width_for_close_button
          tab_rounding: tab_rounding
          touch_extra_padding: touch_extra_padding
          window_border_size: window_border_size
          window_menu_button_position: window_menu_button_position
          window_min_size: window_min_size
          window_padding: window_padding
          window_rounding: window_rounding
          window_title_align: window_title_align

          @staticmethod
          def color(): ...

          @staticmethod
          def create(): ...

        class ImGuiError:
          args: args

          @staticmethod
          def add_note(): ...

          @staticmethod
          def with_traceback(): ...

        class Vec2:
          _field_defaults: dict
          _fields: tuple
          x: _tuplegetter
          y: _tuplegetter

          @staticmethod
          def _asdict(self): ...

          @staticmethod
          def _make(iterable): ...

          @staticmethod
          def _replace(self, **kwds): ...

          @staticmethod
          def count(self, value): ...

          @staticmethod
          def index(self, value, start=0, stop=9223372036854775807): ...

        class Vec4:
          _field_defaults: dict
          _fields: tuple
          w: _tuplegetter
          x: _tuplegetter
          y: _tuplegetter
          z: _tuplegetter

          @staticmethod
          def _asdict(self): ...

          @staticmethod
          def _make(iterable): ...

          @staticmethod
          def _replace(self, **kwds): ...

          @staticmethod
          def count(self, value): ...

          @staticmethod
          def index(self, value, start=0, stop=9223372036854775807): ...

        class _BeginEnd:
          expanded: expanded
          opened: opened

        class _BeginEndChild:
          visible: visible

        class _BeginEndCombo:
          opened: opened

        class _BeginEndDragDropSource:
          dragging: dragging

        class _BeginEndDragDropTarget:
          hovered: hovered

        class _BeginEndGroup: ...

        class _BeginEndListBox:
          opened: opened

        class _BeginEndMainMenuBar:
          opened: opened

        class _BeginEndMenu:
          opened: opened

        class _BeginEndMenuBar:
          opened: opened

        class _BeginEndPopup:
          opened: opened

        class _BeginEndPopupModal:
          opened: opened
          visible: visible

        class _BeginEndTabBar:
          opened: opened

        class _BeginEndTabItem:
          opened: opened
          selected: selected

        class _BeginEndTable:
          opened: opened

        class _BeginEndTooltip: ...

        class _Colors: ...

        class _DrawCmd:
          clip_rect: clip_rect
          elem_count: elem_count
          texture_id: texture_id

        class _DrawData:
          cmd_count: cmd_count
          commands_lists: commands_lists
          display_pos: display_pos
          display_size: display_size
          frame_buffer_scale: frame_buffer_scale
          total_idx_count: total_idx_count
          total_vtx_count: total_vtx_count
          valid: valid

          @staticmethod
          def _require_pointer(): ...

          @staticmethod
          def deindex_all_buffers(): ...

          @staticmethod
          def scale_clip_rects(): ...

        class _DrawList:
          cmd_buffer_data: cmd_buffer_data
          cmd_buffer_size: cmd_buffer_size
          commands: commands
          flags: flags
          idx_buffer_data: idx_buffer_data
          idx_buffer_size: idx_buffer_size
          vtx_buffer_data: vtx_buffer_data
          vtx_buffer_size: vtx_buffer_size

          @staticmethod
          def add_bezier_cubic(): ...

          @staticmethod
          def add_bezier_quadratic(): ...

          @staticmethod
          def add_circle(): ...

          @staticmethod
          def add_circle_filled(): ...

          @staticmethod
          def add_image(): ...

          @staticmethod
          def add_image_rounded(): ...

          @staticmethod
          def add_line(): ...

          @staticmethod
          def add_ngon(): ...

          @staticmethod
          def add_ngon_filled(): ...

          @staticmethod
          def add_polyline(): ...

          @staticmethod
          def add_quad(): ...

          @staticmethod
          def add_quad_filled(): ...

          @staticmethod
          def add_rect(): ...

          @staticmethod
          def add_rect_filled(): ...

          @staticmethod
          def add_rect_filled_multicolor(): ...

          @staticmethod
          def add_text(): ...

          @staticmethod
          def add_triangle(): ...

          @staticmethod
          def add_triangle_filled(): ...

          @staticmethod
          def channels_merge(): ...

          @staticmethod
          def channels_set_current(): ...

          @staticmethod
          def channels_split(): ...

          @staticmethod
          def get_clip_rect_max(): ...

          @staticmethod
          def get_clip_rect_min(): ...

          @staticmethod
          def path_arc_to(): ...

          @staticmethod
          def path_arc_to_fast(): ...

          @staticmethod
          def path_clear(): ...

          @staticmethod
          def path_fill_convex(): ...

          @staticmethod
          def path_line_to(): ...

          @staticmethod
          def path_rect(): ...

          @staticmethod
          def path_stroke(): ...

          @staticmethod
          def pop_clip_rect(): ...

          @staticmethod
          def pop_texture_id(): ...

          @staticmethod
          def prim_quad_UV(): ...

          @staticmethod
          def prim_rect(): ...

          @staticmethod
          def prim_rect_UV(): ...

          @staticmethod
          def prim_reserve(): ...

          @staticmethod
          def prim_unreserve(): ...

          @staticmethod
          def prim_vtx(): ...

          @staticmethod
          def prim_write_idx(): ...

          @staticmethod
          def prim_write_vtx(): ...

          @staticmethod
          def push_clip_rect(): ...

          @staticmethod
          def push_clip_rect_full_screen(): ...

          @staticmethod
          def push_texture_id(): ...

        class _Font: ...

        class _FontAtlas:
          texture_desired_width: texture_desired_width
          texture_height: texture_height
          texture_id: texture_id
          texture_width: texture_width

          @staticmethod
          def _require_pointer(): ...

          @staticmethod
          def add_font_default(): ...

          @staticmethod
          def add_font_from_file_ttf(): ...

          @staticmethod
          def clear(): ...

          @staticmethod
          def clear_fonts(): ...

          @staticmethod
          def clear_input_data(): ...

          @staticmethod
          def clear_tex_data(): ...

          @staticmethod
          def get_glyph_ranges_chinese(): ...

          @staticmethod
          def get_glyph_ranges_chinese_full(): ...

          @staticmethod
          def get_glyph_ranges_cyrillic(): ...

          @staticmethod
          def get_glyph_ranges_default(): ...

          @staticmethod
          def get_glyph_ranges_japanese(): ...

          @staticmethod
          def get_glyph_ranges_korean(): ...

          @staticmethod
          def get_glyph_ranges_latin(): ...

          @staticmethod
          def get_glyph_ranges_thai(): ...

          @staticmethod
          def get_glyph_ranges_vietnamese(): ...

          @staticmethod
          def get_tex_data_as_alpha8(): ...

          @staticmethod
          def get_tex_data_as_rgba32(): ...

        class _IO:
          backend_flags: backend_flags
          config_cursor_blink: config_cursor_blink
          config_drag_click_to_input_text: config_drag_click_to_input_text
          config_flags: config_flags
          config_mac_osx_behaviors: config_mac_osx_behaviors
          config_memory_compact_timer: config_memory_compact_timer
          config_windows_move_from_title_bar_only: config_windows_move_from_title_bar_only
          config_windows_resize_from_edges: config_windows_resize_from_edges
          delta_time: delta_time
          display_fb_scale: display_fb_scale
          display_size: display_size
          font_allow_user_scaling: font_allow_user_scaling
          font_global_scale: font_global_scale
          fonts: fonts
          framerate: framerate
          get_clipboard_text_fn: get_clipboard_text_fn
          ini_file_name: ini_file_name
          ini_saving_rate: ini_saving_rate
          key_alt: key_alt
          key_ctrl: key_ctrl
          key_map: key_map
          key_repeat_delay: key_repeat_delay
          key_repeat_rate: key_repeat_rate
          key_shift: key_shift
          key_super: key_super
          keys_down: keys_down
          log_file_name: log_file_name
          metrics_active_allocations: metrics_active_allocations
          metrics_active_windows: metrics_active_windows
          metrics_render_indices: metrics_render_indices
          metrics_render_vertices: metrics_render_vertices
          metrics_render_windows: metrics_render_windows
          mouse_delta: mouse_delta
          mouse_double_click_max_distance: mouse_double_click_max_distance
          mouse_double_click_time: mouse_double_click_time
          mouse_down: mouse_down
          mouse_drag_threshold: mouse_drag_threshold
          mouse_draw_cursor: mouse_draw_cursor
          mouse_pos: mouse_pos
          mouse_wheel: mouse_wheel
          mouse_wheel_horizontal: mouse_wheel_horizontal
          nav_active: nav_active
          nav_inputs: nav_inputs
          nav_visible: nav_visible
          set_clipboard_text_fn: set_clipboard_text_fn
          want_capture_keyboard: want_capture_keyboard
          want_capture_mouse: want_capture_mouse
          want_save_ini_settings: want_save_ini_settings
          want_set_mouse_pos: want_set_mouse_pos
          want_text_input: want_text_input

          @staticmethod
          def add_input_character(): ...

          @staticmethod
          def add_input_character_utf16(): ...

          @staticmethod
          def add_input_characters_utf8(): ...

          @staticmethod
          def clear_input_characters(): ...

        class _ImGuiContext:
          _keepalive_cache: list

        class _ImGuiInputTextCallbackData:
          buffer: buffer
          buffer_dirty: buffer_dirty
          buffer_size: buffer_size
          buffer_text_length: buffer_text_length
          cursor_pos: cursor_pos
          event_char: event_char
          event_flag: event_flag
          event_key: event_key
          flags: flags
          selection_end: selection_end
          selection_start: selection_start
          user_data: user_data

          @staticmethod
          def _require_pointer(): ...

          @staticmethod
          def clear_selection(): ...

          @staticmethod
          def delete_chars(): ...

          @staticmethod
          def has_selection(): ...

          @staticmethod
          def insert_chars(): ...

          @staticmethod
          def select_all(): ...

        class _ImGuiSizeCallbackData:
          current_size: current_size
          desired_size: desired_size
          pos: pos
          user_data: user_data

          @staticmethod
          def _require_pointer(): ...

        class _ImGuiTableColumnSortSpecs:
          column_index: column_index
          column_user_id: column_user_id
          sort_direction: sort_direction
          sort_order: sort_order

          @staticmethod
          def _require_pointer(): ...

        class _ImGuiTableColumnSortSpecs_array:
          @staticmethod
          def _require_pointer(): ...

        class _ImGuiTableSortSpecs:
          specs: specs
          specs_count: specs_count
          specs_dirty: specs_dirty

          @staticmethod
          def _require_pointer(): ...

        class _ImGuiViewport:
          flags: flags
          pos: pos
          size: size
          work_pos: work_pos
          work_size: work_size

          @staticmethod
          def _require_pointer(): ...

          @staticmethod
          def get_center(): ...

          @staticmethod
          def get_work_center(): ...

        class _InputTextSharedBuffer: ...

        class _StaticGlyphRanges: ...

        class _callback_user_info:
          @staticmethod
          def populate(): ...

        class zip_longest: ...

    class internal:
      AXIS_NONE: int
      AXIS_X: int
      AXIS_Y: int
      BUTTON_ALIGN_TEXT_BASE_LINE: int
      BUTTON_ALLOW_ITEM_OVERLAP: int
      BUTTON_DISABLED: int
      BUTTON_DONT_CLOSE_POPUPS: int
      BUTTON_FLATTEN_CHILDREN: int
      BUTTON_NO_HOLDING_ACTIVE_ID: int
      BUTTON_NO_HOVERED_ON_FOCUS: int
      BUTTON_NO_KEY_MODIFIERS: int
      BUTTON_NO_NAV_FOCUS: int
      BUTTON_PRESSED_ON_CLICK: int
      BUTTON_PRESSED_ON_CLICK_RELEASE: int
      BUTTON_PRESSED_ON_CLICK_RELEASE_ANYWHERE: int
      BUTTON_PRESSED_ON_DEFAULT: int
      BUTTON_PRESSED_ON_DOUBLE_CLICK: int
      BUTTON_PRESSED_ON_DRAG_DROP_HOLD: int
      BUTTON_PRESSED_ON_MASK: int
      BUTTON_PRESSED_ON_RELEASE: int
      BUTTON_REPEAT: int
      INPUT_READ_MODE_DOWN: int
      INPUT_READ_MODE_PRESSED: int
      INPUT_READ_MODE_RELEASED: int
      INPUT_READ_MODE_REPEAT: int
      INPUT_READ_MODE_REPEAT_FAST: int
      INPUT_READ_MODE_REPEAT_SLOW: int
      INPUT_SOURCE_COUNT: int
      INPUT_SOURCE_GAMEPAD: int
      INPUT_SOURCE_KEYBOARD: int
      INPUT_SOURCE_MOUSE: int
      INPUT_SOURCE_NAV: int
      INPUT_SOURCE_NONE: int
      ITEM_BUTTON_REPEAT: int
      ITEM_DEFAULT: int
      ITEM_DISABLED: int
      ITEM_MIXED_VALUE: int
      ITEM_NONE: int
      ITEM_NO_NAV: int
      ITEM_NO_NAV_DEFAULT_FOCUS: int
      ITEM_NO_TAB_STOP: int
      ITEM_READ_ONLY: int
      ITEM_SELECTABLE_DONT_CLOSE_POPUP: int
      ITEM_STATUS_DEACTIVATED: int
      ITEM_STATUS_EDITED: int
      ITEM_STATUS_HAS_DEACTIVATED: int
      ITEM_STATUS_HAS_DISPLAY_RECT: int
      ITEM_STATUS_HOVERED_RECT: int
      ITEM_STATUS_NONE: int
      ITEM_STATUS_TOGGLED_OPEN: int
      ITEM_STATUS_TOGGLED_SELECTION: int
      LAYOUT_TYPE_HORIZONTAL: int
      LAYOUT_TYPE_VERTICAL: int
      LOG_TYPE_LOG_TYPE_BUFFER: int
      LOG_TYPE_LOG_TYPE_CLIPBOARD: int
      LOG_TYPE_LOG_TYPE_FILE: int
      LOG_TYPE_LOG_TYPE_TTY: int
      LOG_TYPE_NONE: int
      NAV_DIR_SOURCE_KEYBOARD: int
      NAV_DIR_SOURCE_NONE: int
      NAV_DIR_SOURCE_PAD_D_PAD: int
      NAV_DIR_SOURCE_PAD_L_STICK: int
      NAV_FORWARD_FORWARD_ACTIVE: int
      NAV_FORWARD_FORWARD_QUEUED: int
      NAV_FORWARD_NONE: int
      NAV_HIGHLIGHT_ALWAYS_DRAW: int
      NAV_HIGHLIGHT_NONE: int
      NAV_HIGHLIGHT_NO_ROUNDING: int
      NAV_HIGHLIGHT_TYPE_DEFAULT: int
      NAV_HIGHLIGHT_TYPE_THIN: int
      NAV_LAYER_COUNT: int
      NAV_LAYER_MAIN: int
      NAV_LAYER_MENU: int
      NAV_MOVE_ALLOW_CURRENT_NAV_ID: int
      NAV_MOVE_ALSO_SCORE_VISIBLE_SET: int
      NAV_MOVE_LOOP_X: int
      NAV_MOVE_LOOP_Y: int
      NAV_MOVE_NONE: int
      NAV_MOVE_SCROLL_TO_EDGE: int
      NAV_MOVE_WRAP_X: int
      NAV_MOVE_WRAP_Y: int
      NEXT_ITEM_DATA_HAS_OPEN: int
      NEXT_ITEM_DATA_HAS_WIDTH: int
      NEXT_ITEM_DATA_NONE: int
      NEXT_WINDOW_DATA_HAS_BACKGROUND_ALPHA: int
      NEXT_WINDOW_DATA_HAS_COLLAPSED: int
      NEXT_WINDOW_DATA_HAS_CONTENT_SIZE: int
      NEXT_WINDOW_DATA_HAS_FOCUS: int
      NEXT_WINDOW_DATA_HAS_POS: int
      NEXT_WINDOW_DATA_HAS_SCROLL: int
      NEXT_WINDOW_DATA_HAS_SIZE: int
      NEXT_WINDOW_DATA_HAS_SIZE_CONSTRAINT: int
      NEXT_WINDOW_DATA_NONE: int
      OLD_COLUMNS_GROW_PARENT_CONTENTS_SIZE: int
      OLD_COLUMNS_NONE: int
      OLD_COLUMNS_NO_BORDER: int
      OLD_COLUMNS_NO_FORCE_WIDTHIN_WINDOW: int
      OLD_COLUMNS_NO_PRESERVE_WIDTHS: int
      OLD_COLUMNS_NO_RESIZE: int
      PLOT_TYPE_HISTOGRAM: int
      PLOT_TYPE_LINES: int
      POPUP_POSITION_POLICY_COMBO_BOX: int
      POPUP_POSITION_POLICY_DEFAULT: int
      POPUP_POSITION_POLICY_TOOLTIP: int
      SELECTABLE_DRAW_HOVERED_WHEN_HELD: int
      SELECTABLE_NO_HOLDING_ACTIVE_ID: int
      SELECTABLE_NO_PAD_WIDHT_HALF_SPACING: int
      SELECTABLE_SELECT_ON_CLICK: int
      SELECTABLE_SELECT_ON_RELEASE: int
      SELECTABLE_SET_NAV_ID_ON_HOVER: int
      SELECTABLE_SPAN_AVAILABLE_WIDTH: int
      SEPARATOR_HORIZONTAL: int
      SEPARATOR_NONE: int
      SEPARATOR_SPAN_ALL_COLUMNS: int
      SEPARATOR_VERTICAL: int
      SLIDER_READ_ONLY: int
      SLIDER_VERTICAL: int
      TAB_BAR_DOCK_NODE: int
      TAB_BAR_IS_FOCUSED: int
      TAB_BAR_SAVE_SETTINGS: int
      TAB_ITEM_BUTTON: int
      TAB_ITEM_NO_CLOSE_BUTTON: int
      TEXT_NONE: int
      TEXT_NO_WIDTH_FRO_LARGE_CLIPPED_TEXT: int
      TOOLTIP_NONE: int
      TOOLTIP_OVERRIDE_PREVIOUS_TOOLTIP: int
      TREE_NODE_CLIP_LABEL_FOR_TRAILING_BUTTON: int

      @staticmethod
      def namedtuple(typename, field_names, rename=False, defaults=None, module=None): ...

      @staticmethod
      def pop_item_flag(): ...

      @staticmethod
      def push_item_flag(): ...

      class ImGuiError:
        args: args

        @staticmethod
        def add_note(): ...

        @staticmethod
        def with_traceback(): ...

      class Vec2:
        _field_defaults: dict
        _fields: tuple
        x: _tuplegetter
        y: _tuplegetter

        @staticmethod
        def _asdict(self): ...

        @staticmethod
        def _make(iterable): ...

        @staticmethod
        def _replace(self, **kwds): ...

        @staticmethod
        def count(self, value): ...

        @staticmethod
        def index(self, value, start=0, stop=9223372036854775807): ...

      class Vec4:
        _field_defaults: dict
        _fields: tuple
        w: _tuplegetter
        x: _tuplegetter
        y: _tuplegetter
        z: _tuplegetter

        @staticmethod
        def _asdict(self): ...

        @staticmethod
        def _make(iterable): ...

        @staticmethod
        def _replace(self, **kwds): ...

        @staticmethod
        def count(self, value): ...

        @staticmethod
        def index(self, value, start=0, stop=9223372036854775807): ...

    class FontConfig: ...

    class GlyphRanges: ...

    class GuiStyle:
      alpha: alpha
      anti_aliased_fill: anti_aliased_fill
      anti_aliased_line_use_tex: anti_aliased_line_use_tex
      anti_aliased_lines: anti_aliased_lines
      button_text_align: button_text_align
      cell_padding: cell_padding
      child_border_size: child_border_size
      child_rounding: child_rounding
      circle_segment_max_error: circle_segment_max_error
      circle_tessellation_max_error: circle_tessellation_max_error
      color_button_position: color_button_position
      colors: colors
      columns_min_spacing: columns_min_spacing
      curve_tessellation_tolerance: curve_tessellation_tolerance
      display_safe_area_padding: display_safe_area_padding
      display_window_padding: display_window_padding
      frame_border_size: frame_border_size
      frame_padding: frame_padding
      frame_rounding: frame_rounding
      grab_min_size: grab_min_size
      grab_rounding: grab_rounding
      indent_spacing: indent_spacing
      item_inner_spacing: item_inner_spacing
      item_spacing: item_spacing
      log_slider_deadzone: log_slider_deadzone
      mouse_cursor_scale: mouse_cursor_scale
      popup_border_size: popup_border_size
      popup_rounding: popup_rounding
      scrollbar_rounding: scrollbar_rounding
      scrollbar_size: scrollbar_size
      selectable_text_align: selectable_text_align
      tab_border_size: tab_border_size
      tab_min_width_for_close_button: tab_min_width_for_close_button
      tab_rounding: tab_rounding
      touch_extra_padding: touch_extra_padding
      window_border_size: window_border_size
      window_menu_button_position: window_menu_button_position
      window_min_size: window_min_size
      window_padding: window_padding
      window_rounding: window_rounding
      window_title_align: window_title_align

      @staticmethod
      def color(): ...

      @staticmethod
      def create(): ...

    class ImGuiError:
      args: args

      @staticmethod
      def add_note(): ...

      @staticmethod
      def with_traceback(): ...

    class Vec2:
      _field_defaults: dict
      _fields: tuple
      x: _tuplegetter
      y: _tuplegetter

      @staticmethod
      def _asdict(self): ...

      @staticmethod
      def _make(iterable): ...

      @staticmethod
      def _replace(self, **kwds): ...

      @staticmethod
      def count(self, value): ...

      @staticmethod
      def index(self, value, start=0, stop=9223372036854775807): ...

    class Vec4:
      _field_defaults: dict
      _fields: tuple
      w: _tuplegetter
      x: _tuplegetter
      y: _tuplegetter
      z: _tuplegetter

      @staticmethod
      def _asdict(self): ...

      @staticmethod
      def _make(iterable): ...

      @staticmethod
      def _replace(self, **kwds): ...

      @staticmethod
      def count(self, value): ...

      @staticmethod
      def index(self, value, start=0, stop=9223372036854775807): ...

    class zip_longest: ...
except NameError:
  exec('ImguiType = ...')

class ProductsPage:

    def __init__(self):
        self.link = None
        self.products = []
        self.page_number = None

    def dict(self):
        representation = {}
        attrs = dir(self)
        for attr in attrs:
            if attr.startswith("__") or attr == "dict":
                continue
            representation[attr] = eval(f"self.{attr}")
        return representation

    def __repr__(self):
        from commands import Print
        pretty = Print.prettify(self.dict(), quiet=True)
        return f"Item: \n{pretty}"


class Product:

    def __init__(self):
        self.link = None
        self.name = None
        self.items = []


    def dict(self):
        representation = {}
        attrs = dir(self)
        for attr in attrs:
            if attr.startswith("__") or attr == "dict":
                continue
            representation[attr] = eval(f"self.{attr}")
        return representation

    def __repr__(self):
        from commands import Print
        pretty = Print.prettify(self.dict(), quiet=True)
        return f"Item: \n{pretty}"


class Item:
    link = None

    name = None
    id = None
    code = None
    capacity = None
    color = None

    photo = None
    grade_brz = None
    grade_brz_verbose = None
    battery_percent = None
    defect = None
    included = None
    case_state = None
    display_state = None
    warranty = None

    certificate_link = None

    imei1 = None
    imei2 = None
    sn = None
    os_version = None
    build_version = None
    firmware = None
    region = None
    spec = None
    carrier = None
    model = None
    mpn = None
    vendor_state = None
    last_nsys_tested = None
    nsys_certificated = None
    battery_health = None
    battery_cycle = None

    fmip = None
    jail = None
    mdm = None
    esn = None
    esnd = None
    sim_lock = None
    purchase_date = None
    coverage_date = None
    supplier = None
    invoice = None
    grade_nsys = None
    note = None

    front_camera = None
    back_camera = None
    telephoto_camera = None
    flash = None
    three_d_touch = None
    touchscreen = None
    loud_speaker = None
    speaker = None
    front_microphone = None
    video_microphone = None
    bottom_microphone = None
    vibration = None
    lcd_pixels = None
    barometer = None
    accelerometer = None
    compass = None
    gyroscope = None
    geolocation = None
    network = None
    bluetooth = None
    wifi = None
    sim_reader = None
    proximity = None
    light_sensor = None
    volume_down = None
    volume_up = None
    home_button = None
    ring_silent_button = None
    face_touch_id = None
    multi_touch = None

    is_motherboard_original = None
    is_battery_original = None
    is_front_camera_original = None
    is_back_camera_original = None
    is_display_original = None
    is_touch_id_original = None

    def dict(self):
        representation = {}
        attrs = dir(self)
        for attr in attrs:
            if attr.startswith("__") or attr == "dict":
                continue
            representation[attr] = eval(f"self.{attr}")
        return representation

    def __repr__(self):
        from commands import Print
        pretty = Print.prettify(self.dict(), quiet=True)
        return f"Item: \n{pretty}"

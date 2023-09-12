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

    def __init__(self):
        self.link = None

        self.name = None
        self.id = None
        self.code = None
        self.capacity = None
        self.color = None

        self.photo = None
        self.grade_brz = None
        self.grade_brz_verbose = None
        self.battery_percent = None
        self.defect = None
        self.included = None
        self.case_state = None
        self.display_state = None
        self.warranty = None

        self.certificate_link = None

        self.imei1 = None
        self.imei2 = None
        self.sn = None
        self.os_version = None
        self.build_version = None
        self.firmware = None
        self.region = None
        self.spec = None
        self.carrier = None
        self.model = None
        self.mpn = None
        self.vendor_state = None
        self.last_nsys_tested = None
        self.nsys_certificated = None
        self.battery_health = None
        self.battery_cycle = None

        self.fmip = None
        self.jail = None
        self.mdm = None
        self.esn = None
        self.esnd = None
        self.sim_lock = None
        self.purchase_date = None
        self.coverage_date = None
        self.supplier = None
        self.invoice = None
        self.grade_nsys = None
        self.note = None

        self.front_camera = None
        self.back_camera = None
        self.telephoto_camera = None
        self.flash = None
        self.three_d_touch = None
        self.touchscreen = None
        self.loud_speaker = None
        self.speaker = None
        self.front_microphone = None
        self.video_microphone = None
        self.bottom_microphone = None
        self.vibration = None
        self.lcd_pixels = None
        self.barometer = None
        self.accelerometer = None
        self.compass = None
        self.gyroscope = None
        self.geolocation = None
        self.network = None
        self.bluetooth = None
        self.wifi = None
        self.sim_reader = None
        self.proximity = None
        self.light_sensor = None
        self.volume_down = None
        self.volume_up = None
        self.home_button = None
        self.ring_silent_button = None
        self.face_touch_id = None
        self.multi_touch = None

        self.is_motherboard_original = None
        self.is_battery_original = None
        self.is_front_camera_original = None
        self.is_back_camera_original = None
        self.is_display_original = None
        self.is_touch_id_original = None

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

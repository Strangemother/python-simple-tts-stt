import os


class Effect(object):

    keys = None

    def get_keys(self):
        if self.keys is not None:
            return self.keys
        self_class = self._ref if hasattr(self, '_ref') else self.__class__
        return tuple(set(dir(self)) - set(dir(self_class)))

    def __init__(self, *args, **kwargs):
        self.kw = kwargs
        ordered_attrs = self.kw.get('keys', self.get_keys())

        args_kw = {}

        for order_key, index in zip(ordered_attrs, range(len(ordered_attrs))):
            try:
                val = args[index]
            except IndexError:
                val = kwargs.get(order_key, None)
                if val is None:
                    val = getattr(self, order_key)

            args_kw[order_key] = val

        kwargs.update(args_kw)

        for k in kwargs:
            setattr(self, k, kwargs[k])

        # super(cls, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.get_keys())


class ChorusEffect(Effect):

    delay = 40
    decay = .4
    speed = .7
    depth = 2


class Filter(Effect):
    """An abstraction of an FFMpeg filter string = given to the ffmpeg cli.

        Chorus().as_String()
    """
    name = None
    # Set input gain. Default is 0.4.
    in_gain = '0.4'

    # Set output gain. Default is 0.4.
    out_gain = '0.5'

    template = None

    keys =(
        'in_gain',
        'out_gain',
        "delay",
        "decay",
     )

    effects = None

    # def __init__(self, *args, **kwargs):
    #     super(Filter, self).__init__(*args, **kwargs)

    def get_name(self):
        if self.name is None:
            return self.__class__.__name__.lower()

        return self.name

    def get_effects(self):
        res = self.kw.get('effects', None) or self.effects

        if res is None:
            # No effects list is applied- the elements required exist on
            # the given filter
            res = (Effect(keys=self.get_keys(), **{x: getattr(self, x) for x in self.keys}),)
        return res

    def as_string(self):
        """Merge all the effects into a string using the template."""
        effects_list = self.get_effects()
        kwo = {}

        for key in self.keys:
            kwo[key] = get_stack(key, effects_list)

        template = self.get_template()

        templated = template.format(**kwo)

        return templated

    def get_template(self):
        existing = self.template
        res_str = "{}={}"
        keys =self.keys

        print('\n  -- template for',self, keys)
        if existing is None:
            existing = ":".join(["{%s}" % x for x in keys])
        return res_str.format(self.get_name(), existing)


class Chorus(Filter):

    # template ='chorus={in_gain}:{out_gain}:{delay}:{decay}:{speed}:{depth}'
    keys =( 'in_gain',
            'out_gain',
            "delay",
            "decay",
            "speed",
            "depth",
        )

    delay = 40
    decay = .4
    speed = .7
    depth = 2

    #effects = (
        #ChorusEffect(10, 0.4, 0.7, 2),
        #ChorusEffect(140, 0.4, 0.8, 0.8),
        #Effect(30, 0.5, 0.7, 1.3),
        # Effect(50, 1, 0.9, 0.4),
        # Effect(10, 0.7, 0.6, .7),
        # Effect(20, 0.4, 0.2, 2.2),
        # Effect(60, 0.6, 0.7, 1),
   # )


class Echo(Filter):
    name = 'aecho'

    keys = ('in_gain', 'out_gain', 'delay', 'decay', )
    # template= "aecho={in_gain}:{out_gain}:{delays}:{decay}"

    # def as_string(self):
    #     return "aecho=0.8:0.88:6:0.4"


    #Set input gain of reflected signal. Default is .6
    in_gain=.6

    #Set output gain of reflected signal. Default is .3
    out_gain=.3

    #Set list of time intervals in milliseconds between original signal
    #and reflections separated by '|'. Allowed range for each delay is
    # (0 - 90000.0]. Default is
    delay= 500

    # Set list of loudness of reflected signals separated by '|'.
    # Allowed range for each decay is (0 - 1.0]. Default is 0.5.
    decay = 0.5


class Flang(Filter):

    name='flanger'

    keys = (
        "delay",
        "depth",
        "regen",
        "width",
        "speed",
        "shape",
        "phase",
        "interp",
    )

    # Set base delay in milliseconds. Range from 0 to 30.
    # Default value is 0.
    delay = 0

    # Set added sweep delay in milliseconds. Range from 0 to 10.
    # Default value is 2.
    depth = 2

    # Set percentage regeneration (delayed signal feedback). Range from -95 to 95.
    # Default value is 0.
    regen = 0

    # Set percentage of delayed signal mixed with original. Range from 0 to 100.
    # Default value is 71.
    width = 71

    # Set sweeps per second (Hz). Range from 0.1 to 10.
    # Default value is 0.5.
    speed = .5

    # Set swept wave shape, can be 'triangular' or 'sinusoidal'.
    # Default value is sinusoidal.
    shape = 'sinusoidal'

    # Set swept wave percentage-shift for multi channel. Range from 0 to 100.
    # Default value is 25.
    phase = 25

    # Set delay-line interpolation, linear or quadratic.
    # Default is linear.
    interp = 'linear'


def get_stack(key, effect_set):
    """Given a list of effects from an efect_list, extract the given `key`
    value from each object and return a string joined with a pipe `|`.

    This is used for merging many similay effects as one string

        get_stack('delay', [ChorusEffect(),ChorusEffect(),])
        ".8|.8"
    """
    r = []
    for item in effect_set:
        r.append(str(getattr(item, key)))
    return '|'.join(r)


def create_filter_string(filters=None):

    filters = filters or (
        Chorus(),
        #Echo,
        #Flang,
        # "aecho=0.5:0.9:20:0.5",
    )

    # chorus = Chorus().as_string()
    # # robotic
    # aecho= Echo().as_string()
    # # doubling
    # aecho="aecho=0.5:0.9:20:0.5"

    strings = ()

    for item in filters:
        if callable(item):
            item = item()

        res = item
        if hasattr(item, 'as_string'):
            res = item.as_string()
        strings += (res, )

    if len(strings) == 0:
        filter_str = ''
    else:
        filter_str = ', '.join(strings)
        filter_str ='-filter_complex "{}"'.format(filter_str)


    print('\n  -- filter_string', filter_str)
    return filter_str


def play_file(filepath):
    print('\nPlaying')
    fs = 'start {}'.format(filepath)
    print(fs)
    os.system(fs)

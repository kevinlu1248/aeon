# -*- coding: utf-8 -*-
# The key string (i.e. 'euclidean') must be the same as the name in _registry

_expected_distance_results = {
    # Result structure:
    # [single value series, univariate series, multivariate series, dataset,
    #   unequal univariate, multivariate unequal, dataset unequal]
    "euclidean": [
        5.0,
        2.6329864895136623,
        7.093596608755006,
        70.56413351420169,
        2.3179478388647876,
        4.938969178714248,
        49.694052115721675,
    ],
    "erp": [5.0, 5.037672883414786, 20.724482073800456, 208.797697936059,
            5.16666987535642, 18.353616712062177, 171.1112853298397],
    "edr": [1.0, 0.6, 1.0],
    "lcss": [1.0, 0.09999999999999998, 1.0, 9.8, 0.0, 1.0, 9.4],
    "squared": [
        25.0,
        6.932617853961479,
        50.31911284774053,
        499.6749760624051,
        5.37288218369794,
        24.39341654828929,
        247.6996067496993,
    ],
    "dtw": [
        25.0,
        2.180365495972097,
        47.59969618998147,
        461.05467389005753,
        4.360373075383168,
        44.86527164702194,
        403.49548197391704,
    ],
    "ddtw": [
        0.0,
        2.0884818837222006,
        34.837800040564005,
        323.279387211988,
        3.6475610211489875,
        35.916981095128804,
        281.92058999075414,
    ],
    "wdtw": [
        12.343758137512241,
        0.985380547171357,
        21.265839226825413,
        205.30721939046768,
        2.0040890166976926,
        20.795690703034445,
        189.3408257880001,
    ],
    "wddtw": [
        0.0,
        0.9736009365730778,
        15.926194649221529,
        147.3253061156872,
        1.7031094916423124,
        16.967390011736825,
        135.38765623045913,
    ],
    "msm": [5.0, 6.828557434224288, None],
    "twe": [5.0, 11.548698748091073, 39.87793560457224],
}

_expected_distance_results_params = {
    # Result structure:
    # [univariate series, multivariate series]
    "dtw": [
        [3.088712375990371, 47.59969618998147],
    ],
    "erp": [
        [0.6648081862148058, 4.365472428062562],
        [5.279748833082764, 20.71830043391765],
    ],
    "edr": [
        [0.3, 0.3],
        [0.3, 1.0],
    ],
    "lcss": [
        [0.09999999999999998, 1.0],
        [0.30000000000000004, 1.0],
    ],
    "ddtw": [
        [2.683958998434711, 34.837800040564005],
    ],
    "wdtw": [
        [1.364177898415523, 21.265839226825413],
        [0.02752598656586074, 0.33677832093219406],
    ],
    "wddtw": [
        [1.223806382386346, 15.926194649221529],
        [0.08524969290653987, 0.663028083142974],
    ],
    "twe": [
        [5.260445939887447, 9.230959005394121],
        [10.16824892186273, 38.87793560457224],
        [14.469312584616958, 41.0046466591961],
        [11.548698748091073, 39.87793560457224],
    ],
}

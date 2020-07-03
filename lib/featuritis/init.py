import os
import os.path

import featuritis.constants
import featuritis.exc


def initialize(parent_directory):

    featuritis_path = os.path.join(
        parent_directory,
        featuritis.constants.FEATURITIS_PATH,
    )
    featuritis_config_path = os.path.join(
        parent_directory,
        featuritis.constants.FEATURITIS_CONFIG_PATH
    )

    if os.path.exists(featuritis_path):
        raise featuritis.exc.InitilizationError(
            "{} folder already exists!".format(featuritis_path),
        )

    if os.path.exists(featuritis_config_path):
        raise featuritis.exc.InitilizationError(
            "{} already exists!".format(featuritis_config_path),
        )

    os.mkdir(featuritis_path)

    features_path = os.path.join(featuritis_path, "features")
    os.mkdir(features_path)

    with open(featuritis_config_path, "wt") as fp:
        fp.write("[featuritis]\n")
        fp.write("featuritis_path = featuritis\n")

    return 0

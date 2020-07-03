import datetime
import os.path
import re

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import featuritis.constants
import featuritis.exc


TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"


class Manager(object):

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = featuritis.constants.FEATURITIS_CONFIG_PATH

        if not os.path.exists(config_path):
            raise featuritis.exc.ConfigError(
                "featuritis config {} not found!".format(config_path),
            )

        self.config = ConfigParser()
        self.config.read(config_path)

        self.featuritis_path = self.config["featuritis"]["featuritis_path"]
        self.features_path = os.path.join(self.featuritis_path, "features")

    def get_all_features(self):

        features = {}

        names = os.listdir(self.features_path)

        for name in names:
            full_path = os.path.join(self.features_path, name)

            locs = {}

            with open(full_path, "rt") as fp:
                exec(fp.read(), {}, locs)

            features[locs["feature_id"]] = locs

            if locs["ticketing_system"] is not None:
                ticketing_system = locs["ticketing_system"]
                if ticketing_system in self.config:
                    system_config = self.config[ticketing_system]
                    system = importlib.import_module(system_config["module"])

                    features[locs["feature_id"]]["ticketing"] = system

        return features

    def add(self, feature_id, description=None, author=None, ticketing_system=None):

        features = self.get_all_features()
        if feature_id in features:
             raise featuritis.exc.FeatureExistsError(
                "feature with id {!r} already exists!".format(feature_id),
            )

        feature_time = datetime.datetime.now(tz=datetime.timezone.utc)
        feature_time_formatted = feature_time.strftime(TIMESTAMP_FORMAT)

        feature_id_for_name = re.sub(r'[#:/]', "_", feature_id)

        description_for_name = re.sub(r'[^a-zA-Z0-9_.-]', "_", description)
        description_for_name = re.sub(r'_+', "_", description_for_name)

        filename = "{}_{}_{}.py".format(
            feature_time_formatted,
            feature_id_for_name,
            description_for_name,
        )

        feature_path = os.path.join(self.features_path, filename)

        with open(feature_path, "wt") as fp:
            fp.write("import datetime\n")
            fp.write("\n")
            fp.write("feature_id = {!r}\n".format(feature_id))
            fp.write("timestamp = {!r}\n".format(feature_time))
            fp.write("description = {!r}\n".format(description))
            fp.write("author = {!r}\n".format(author))
            fp.write("ticketing_system = {!r}\n".format(ticketing_system))

        return feature_path

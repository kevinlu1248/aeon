# -*- coding: utf-8 -*-
"""Unit tests for classifier/regressor input output."""

__author__ = ["mloning", "TonyBagnall", "fkiraly"]

import inspect

import numpy as np

from aeon.classification.tests._expected_outputs import (
    basic_motions_proba,
    unit_test_proba,
)
from aeon.datasets import load_basic_motions, load_unit_test
from aeon.datatypes import check_is_scitype
from aeon.tests.test_all_estimators import BaseFixtureGenerator, QuickTester
from aeon.utils._testing.estimator_checks import _assert_array_almost_equal
from aeon.utils._testing.scenarios_classification import ClassifierFitPredict


class ClassifierFixtureGenerator(BaseFixtureGenerator):
    """Fixture generator for classifier tests.

    Fixtures parameterized
    ----------------------
    estimator_class: estimator inheriting from BaseObject
        ranges over estimator classes not excluded by EXCLUDE_ESTIMATORS, EXCLUDED_TESTS
    estimator_instance: instance of estimator inheriting from BaseObject
        ranges over estimator classes not excluded by EXCLUDE_ESTIMATORS, EXCLUDED_TESTS
        instances are generated by create_test_instance class method
    scenario: instance of TestScenario
        ranges over all scenarios returned by retrieve_scenarios
    """

    # note: this should be separate from TestAllClassifiers
    #   additional fixtures, parameters, etc should be added here
    #   Classifiers should contain the tests only

    estimator_type_filter = "classifier"


class TestAllClassifiers(ClassifierFixtureGenerator, QuickTester):
    """Module level tests for all aeon classifiers."""

    def test_classifier_output(self, estimator_instance, scenario):
        """BASE CLASS TEST. Test classifier outputs the correct data types and values.

        Test predict produces a np.array or pd.Series with only values seen in the train
        data, and that predict_proba probability estimates add up to one.
        """
        n_classes = scenario.get_tag("n_classes")
        X_new = scenario.args["predict"]["X"]
        y_train = scenario.args["fit"]["y"]
        # we use check_is_scitype to get the number instances in X_new
        #   this is more robust against different scitypes in X_new
        _, _, X_new_metadata = check_is_scitype(X_new, "Panel", return_metadata=True)
        X_new_instances = X_new_metadata["n_instances"]

        # run fit and predict
        y_pred = scenario.run(estimator_instance, method_sequence=["fit", "predict"])

        # check predict
        assert isinstance(y_pred, np.ndarray)
        assert y_pred.shape == (X_new_instances,)
        assert np.all(np.isin(np.unique(y_pred), np.unique(y_train)))

        # check predict proba (all classifiers have predict_proba by default)
        y_proba = scenario.run(estimator_instance, method_sequence=["predict_proba"])
        assert isinstance(y_proba, np.ndarray)
        assert y_proba.shape == (X_new_instances, n_classes)
        np.testing.assert_almost_equal(y_proba.sum(axis=1), 1, decimal=4)

    def test_classifier_on_unit_test_data(self, estimator_class):
        """Test classifier on unit test data."""
        # we only use the first estimator instance for testing
        classname = estimator_class.__name__

        # retrieve expected predict_proba output, and skip test if not available
        if classname in unit_test_proba.keys():
            expected_probas = unit_test_proba[classname]
        else:
            # skip test if no expected probas are registered
            return None

        # we only use the first estimator instance for testing
        estimator_instance = estimator_class.create_test_instance(
            parameter_set="results_comparison"
        )
        # set random seed if possible
        if "random_state" in estimator_instance.get_params().keys():
            estimator_instance.set_params(random_state=0)

        # load unit test data
        X_train, y_train = load_unit_test(split="train")
        X_test, _ = load_unit_test(split="test")
        indices = np.random.RandomState(0).choice(len(y_train), 10, replace=False)

        # train classifier and predict probas
        estimator_instance.fit(X_train, y_train)
        y_proba = estimator_instance.predict_proba(X_test[indices])
        #

        # assert probabilities are the same
        _assert_array_almost_equal(y_proba, expected_probas, decimal=2)

    def test_classifier_on_basic_motions(self, estimator_class):
        """Test classifier on basic motions data."""
        # we only use the first estimator instance for testing
        classname = estimator_class.__name__

        # retrieve expected predict_proba output, and skip test if not available
        if classname in basic_motions_proba.keys():
            expected_probas = basic_motions_proba[classname]
        else:
            # skip test if no expected probas are registered
            return None

        # we only use the first estimator instance for testing
        estimator_instance = estimator_class.create_test_instance(
            parameter_set="results_comparison"
        )
        # set random seed if possible
        if "random_state" in estimator_instance.get_params().keys():
            estimator_instance.set_params(random_state=0)

        # load unit test data
        X_train, y_train = load_basic_motions(split="train")
        X_test, _ = load_basic_motions(split="test")
        indices = np.random.RandomState(4).choice(len(y_train), 10, replace=False)

        # train classifier and predict probas
        estimator_instance.fit(X_train[indices], y_train[indices])
        y_proba = estimator_instance.predict_proba(X_test[indices])

        # assert probabilities are the same
        _assert_array_almost_equal(y_proba, expected_probas, decimal=2)

    def test_contracted_classifier(self, estimator_class):
        """Test classifiers that can be contracted."""
        if estimator_class.get_class_tag(tag_name="capability:contractable") is True:
            # if we have a train_estimate parameter set use it, else use default
            estimator_instance = estimator_class.create_test_instance(
                parameter_set="contracting"
            )

            # The "capability:contractable" has not been fully implemented yet.
            # Most uses currently have a time_limit_in_minutes parameter, but we won't
            # fail those that don't.
            default_params = inspect.signature(estimator_class.__init__).parameters
            if default_params.get(
                "time_limit_in_minutes", None
            ) is not None and default_params.get(
                "time_limit_in_minutes", None
            ).default not in (
                0,
                -1,
                None,
            ):
                return None

            # too short of a contract time can lead to test failures
            if vars(estimator_instance).get("time_limit_in_minutes", None) < 5:
                raise ValueError(
                    "Test parameters for test_contracted_classifier must set "
                    "time_limit_in_minutes to 5 or more."
                )

            scenario = ClassifierFitPredict()

            X_new = scenario.args["predict"]["X"]
            y_train = scenario.args["fit"]["y"]
            # we use check_is_scitype to get the number instances in X_new
            #   this is more robust against different scitypes in X_new
            _, _, X_new_metadata = check_is_scitype(
                X_new, "Panel", return_metadata=True
            )
            X_new_instances = X_new_metadata["n_instances"]

            # run fit and predict
            y_pred = scenario.run(
                estimator_instance, method_sequence=["fit", "predict"]
            )

            # check predict
            assert isinstance(y_pred, np.ndarray)
            assert y_pred.shape == (X_new_instances,)
            assert np.all(np.isin(np.unique(y_pred), np.unique(y_train)))
        else:
            # skip test if it can't contract
            return None

    def test_classifier_train_estimate(self, estimator_class):
        """Test classifiers that can produce train set probability estimates."""
        if estimator_class.get_class_tag(tag_name="capability:train_estimate") is True:
            # if we have a train_estimate parameter set use it, else use default
            estimator_instance = estimator_class.create_test_instance(
                parameter_set="train_estimate"
            )

            # The "capability:train_estimate" has not been fully implemented yet.
            # Most uses currently have the below method, but we won't fail those that
            # don't.
            if not hasattr(estimator_instance, "_get_train_probs"):
                return None

            # fit classifier
            scenario = ClassifierFitPredict()
            scenario.run(estimator_instance, method_sequence=["fit"])

            n_classes = scenario.get_tag("n_classes")
            X_train = scenario.args["fit"]["X"]
            y_train = scenario.args["fit"]["y"]
            _, _, X_train_metadata = check_is_scitype(
                X_train, "Panel", return_metadata=True
            )
            X_train_len = X_train_metadata["n_instances"]

            # check the probabilities are valid
            train_proba = estimator_instance._get_train_probs(X_train, y_train)
            assert isinstance(train_proba, np.ndarray)
            assert train_proba.shape == (X_train_len, n_classes)
            np.testing.assert_almost_equal(train_proba.sum(axis=1), 1, decimal=4)
        else:
            # skip test if it can't produce an estimate
            return None

    def test_does_not_override_final_methods(self, estimator_class):
        if "fit" in estimator_class.__dict__:
            raise ValueError(f"Classifier {estimator_class} overrides the method fit")
        if "predict" in estimator_class.__dict__:
            raise ValueError(
                f"Classifier {estimator_class} overrides the method " f"predict"
            )
        if "predict_proba" in estimator_class.__dict__:
            raise ValueError(
                f"Classifier {estimator_class} overrides the method " f"predict_proba"
            )

import os

from astropy import units as u
import numpy as np
import pytest

import tardis
from tardis.io.config_reader import Configuration
from tardis.io.model_reader import (
    read_artis_density, read_simple_ascii_abundances, read_simple_isotope_abundances, read_uniform_abundances, read_cmfgen_density)

data_path = os.path.join(tardis.__path__[0], 'io', 'tests', 'data')

@pytest.fixture
def artis_density_fname():
    return os.path.join(data_path, 'artis_model.dat')

@pytest.fixture
def artis_abundances_fname():
    return os.path.join(data_path, 'artis_abundances.dat')


@pytest.fixture
def tardis_model_abundance_fname():
    return os.path.join(data_path, 'tardis_model_abund.csv')


@pytest.fixture
def tardis_model_density_fname():
    return os.path.join(data_path, 'tardis_model_density.dat')


@pytest.fixture
def isotope_uniform_abundance():
    config_path = os.path.join(
        data_path, 'tardis_configv1_isotope_uniabund.yml')
    config = Configuration.from_yaml(config_path)
    return config.model.abundances

def test_simple_read_artis_density(artis_density_fname):
    time_of_model, velocity, mean_density = read_artis_density(artis_density_fname)

    assert np.isclose(0.00114661 * u.day, time_of_model, atol=1e-7 * u.day)
    assert np.isclose(mean_density[23], 0.2250048 * u.g / u.cm**3, atol=1.e-6
        * u.g / u.cm**3)
    assert len(mean_density) == 69
    assert len(velocity) == len(mean_density) + 1

# Artis files are currently read with read ascii files function
def test_read_simple_ascii_abundances(artis_abundances_fname):
    index, abundances = read_simple_ascii_abundances(artis_abundances_fname)
    assert len(abundances.columns) == 69
    assert np.isclose(abundances[23].ix[2], 2.672351e-08 , atol=1.e-12)


def test_read_simple_isotope_abundances(tardis_model_abundance_fname):
    index, abundances, isotope_abundance = read_simple_isotope_abundances(
        tardis_model_abundance_fname)
    assert np.isclose(abundances.loc[6, 9], 0.5, atol=1.e-12)
    assert np.isclose(abundances.loc[12, 6], 0.8, atol=1.e-12)
    assert np.isclose(abundances.loc[14, 2], 0.3, atol=1.e-12)
    assert np.isclose(isotope_abundance.loc[(28, 56), 1], 0.5, atol=1.e-12)
    assert np.isclose(isotope_abundance.loc[(28, 58), 2], 0.7, atol=1.e-12)


def test_read_uniform_abundances(isotope_uniform_abundance):
    abundances, isotope_abundance = read_uniform_abundances(
        isotope_uniform_abundance, 20)
    assert np.isclose(abundances.loc[8, 2], 0.19, atol=1.e-12)
    assert np.isclose(abundances.loc[20, 5], 0.03, atol=1.e-12)
    assert np.isclose(isotope_abundance.loc[(28, 56), 15], 0.05, atol=1.e-12)
    assert np.isclose(isotope_abundance.loc[(28, 58), 2], 0.05, atol=1.e-12)


def test_simple_read_cmfgen_density(tardis_model_density_fname):
    time_of_model, velocity, mean_density, electron_densities, temperature = read_cmfgen_density(
        tardis_model_density_fname)

    assert np.isclose(0.976 * u.day, time_of_model, atol=1e-7 * u.day)
    assert np.isclose(mean_density[3], 2.2411003e-18 * u.g / u.cm**3, atol=1.e-6
                      * u.g / u.cm**3)
    assert np.isclose(electron_densities[5], 49308.29 * u.g / u.cm**3, atol=1.e-6
                      * u.g / u.cm**3)
    assert len(mean_density) == 10
    assert len(velocity) == len(mean_density) + 1

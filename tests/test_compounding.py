import pyquantlib as ql


def test_compounding_values_exist():
    assert hasattr(ql, 'Simple')
    assert hasattr(ql, 'Compounded')
    assert hasattr(ql, 'Continuous')
    assert hasattr(ql, 'SimpleThenCompounded')
    assert hasattr(ql, 'CompoundedThenSimple')


def test_compounding_enum():
    assert ql.Simple == ql.Compounding.Simple
    assert ql.Compounded == ql.Compounding.Compounded
    assert ql.Continuous == ql.Compounding.Continuous

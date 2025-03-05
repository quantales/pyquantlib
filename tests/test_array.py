import pytest
import numpy as np
import math
import pyquantlib as ql


def approx_equal_array(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for x, y in zip(arr1, arr2):
        if not x == pytest.approx(y):
            return False
    return True


# --- Constructors ---

def test_array_default_constructor():
    arr = ql.Array()
    assert isinstance(arr, ql.Array)
    assert len(arr) == 0
    assert arr.empty()


def test_array_size_constructor():
    arr = ql.Array(5)
    assert len(arr) == 5


def test_array_size_value_constructor():
    arr = ql.Array(3, 7.5)
    assert len(arr) == 3
    for i in range(3):
        assert arr[i] == 7.5


def test_array_iterable_constructor():
    data = [1.0, 2.5, -3.0]
    arr = ql.Array(data)
    assert len(arr) == len(data)
    for i in range(len(data)):
        assert arr[i] == data[i]

    arr_tuple = ql.Array((0.5, 1.5))
    assert len(arr_tuple) == 2
    assert arr_tuple[0] == 0.5
    assert arr_tuple[1] == 1.5

    arr_empty = ql.Array([])
    assert len(arr_empty) == 0
    assert arr_empty.empty()


def test_array_numpy_constructor():
    np_data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
    arr = ql.Array(np_data)
    assert len(arr) == len(np_data)
    for i in range(len(np_data)):
        assert arr[i] == np_data[i]

    with pytest.raises(RuntimeError):
        ql.Array(np.array([[1, 2], [3, 4]]))


# --- Buffer protocol ---

def test_array_to_numpy_view():
    data = [1.0, 2.0, 3.0, 4.0]
    ql_arr = ql.Array(data)

    np_view = np.array(ql_arr, copy=False)
    assert np_view.shape == (len(data),)
    assert np.allclose(np_view, data)

    ql_arr[0] = 10.0
    assert np_view[0] == 10.0

    np_view[1] = 20.0
    assert ql_arr[1] == 20.0


def test_array_to_numpy_copy():
    ql_arr = ql.Array([1.0, 2.0, 3.0])
    np_copy = np.array(ql_arr, copy=True)
    np_copy[0] = 99.0
    assert ql_arr[0] != 99.0


# --- Size and capacity ---

def test_array_size_len_empty():
    arr = ql.Array([1, 2, 3])
    assert arr.size() == 3
    assert len(arr) == 3
    assert not arr.empty()

    arr_empty = ql.Array()
    assert arr_empty.size() == 0
    assert len(arr_empty) == 0
    assert arr_empty.empty()


def test_array_resize():
    arr = ql.Array([1, 2, 3])
    arr.resize(5)
    assert len(arr) == 5
    assert arr[0] == 1
    assert arr[1] == 2
    assert arr[2] == 3

    arr.resize(2)
    assert len(arr) == 2
    assert arr[0] == 1
    assert arr[1] == 2

    arr.resize(4, 9.9)
    assert len(arr) == 4
    assert arr[2] == 9.9
    assert arr[3] == 9.9


def test_array_swap():
    arr1 = ql.Array([1, 2])
    arr2 = ql.Array([3, 4, 5])

    arr1_orig = list(arr1)
    arr2_orig = list(arr2)

    arr1.swap(arr2)

    assert list(arr1) == arr2_orig
    assert list(arr2) == arr1_orig


def test_array_fill():
    arr = ql.Array(3)
    arr.fill(5.5)
    assert len(arr) == 3
    for x in arr:
        assert x == 5.5


# --- Element access ---

def test_array_getitem_setitem():
    arr = ql.Array([1.0, 2.0, 3.0])
    assert arr[0] == 1.0
    assert arr[1] == 2.0
    assert arr[2] == 3.0

    arr[1] = 2.5
    assert arr[1] == 2.5

    with pytest.raises(IndexError):
        _ = arr[3]
    with pytest.raises(IndexError):
        arr[3] = 4.0


def test_array_at():
    arr = ql.Array([1.0, 2.0])
    assert arr.at(0) == 1.0
    assert arr.at(1) == 2.0

    with pytest.raises(ql.Error):
        arr.at(2)


def test_array_front_back():
    arr = ql.Array([10.0, 20.0, 30.0])
    assert arr.front() == 10.0
    assert arr.back() == 30.0

    arr_single = ql.Array([5.0])
    assert arr_single.front() == 5.0
    assert arr_single.back() == 5.0

    arr_empty = ql.Array()
    with pytest.raises(IndexError):
        arr_empty.front()
    with pytest.raises(IndexError):
        arr_empty.back()


# --- Iteration ---

def test_array_iteration():
    data = [1.1, 2.2, 3.3]
    arr = ql.Array(data)

    iterated = list(arr)
    assert iterated == data
    assert list(ql.Array([])) == []


# --- Repr ---

def test_array_repr():
    arr = ql.Array([1, 2, 3])
    assert repr(arr) == "Array([1, 2, 3])"

    arr_empty = ql.Array([])
    assert repr(arr_empty) == "Array([])"

    arr_long = ql.Array([float(i) for i in range(20)])
    assert "...," in repr(arr_long)


# --- Operators ---

def test_array_unary_minus():
    arr = ql.Array([1.0, -2.0, 0.0])
    neg_arr = -arr
    assert isinstance(neg_arr, ql.Array)
    assert approx_equal_array(neg_arr, [-1.0, 2.0, 0.0])
    assert approx_equal_array(arr, [1.0, -2.0, 0.0])


def test_array_inplace_operators_array():
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([4, 5, 6])

    arr1 += arr2
    assert approx_equal_array(arr1, [5, 7, 9])

    arr1 = ql.Array([5, 7, 9])
    arr1 -= arr2
    assert approx_equal_array(arr1, [1, 2, 3])

    arr1 = ql.Array([1, 2, 3])
    arr1 *= arr2
    assert approx_equal_array(arr1, [4, 10, 18])

    arr1 = ql.Array([4, 10, 18])
    arr1 /= ql.Array([2, 2, 3])
    assert approx_equal_array(arr1, [2, 5, 6])


def test_array_inplace_operators_scalar():
    arr = ql.Array([1, 2, 3])

    arr += 2.0
    assert approx_equal_array(arr, [3, 4, 5])

    arr -= 1.0
    assert approx_equal_array(arr, [2, 3, 4])

    arr *= 3.0
    assert approx_equal_array(arr, [6, 9, 12])

    arr /= 2.0
    assert approx_equal_array(arr, [3, 4.5, 6])


def test_array_binary_operators_array():
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([4, 5, 6])

    assert approx_equal_array(arr1 + arr2, [5, 7, 9])
    assert approx_equal_array(arr1 - arr2, [-3, -3, -3])
    assert approx_equal_array(arr1 * arr2, [4, 10, 18])
    assert approx_equal_array(ql.Array([4, 10, 18]) / ql.Array([2, 2, 3]), [2, 5, 6])


def test_array_binary_operators_scalar():
    arr = ql.Array([1, 2, 3])

    assert approx_equal_array(arr + 2.0, [3, 4, 5])
    assert approx_equal_array(arr - 1.0, [0, 1, 2])
    assert approx_equal_array(arr * 3.0, [3, 6, 9])
    assert approx_equal_array(arr / 2.0, [0.5, 1.0, 1.5])


def test_array_reverse_scalar_operators():
    arr = ql.Array([1, 2, 3])

    assert approx_equal_array(2.0 + arr, [3, 4, 5])
    assert approx_equal_array(5.0 - arr, [4, 3, 2])
    assert approx_equal_array(3.0 * arr, [3, 6, 9])
    assert approx_equal_array(12.0 / ql.Array([2, 4, 6]), [6.0, 3.0, 2.0])


def test_array_comparison_operators():
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([1, 2, 3])
    arr3 = ql.Array([1, 2, 4])
    arr4 = ql.Array([1, 2])

    assert (arr1 == arr2) is True
    assert (arr1 != arr2) is False
    assert (arr1 == arr3) is False
    assert (arr1 != arr3) is True
    assert (arr1 == arr4) is False
    assert (arr1 != arr4) is True


# --- Math functions ---

def test_array_dot_product():
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([4, 5, 6])
    assert ql.DotProduct(arr1, arr2) == pytest.approx(32.0)

    with pytest.raises(ql.Error):
        ql.DotProduct(arr1, ql.Array([1, 2]))


def test_array_unary_functions():
    arr_pos = ql.Array([1.0, 4.0, 9.0])
    arr_mix = ql.Array([-1.0, 0.0, 2.0])

    assert approx_equal_array(ql.Abs(arr_mix), [1.0, 0.0, 2.0])
    assert approx_equal_array(ql.Sqrt(arr_pos), [1.0, 2.0, 3.0])

    with pytest.raises(ValueError):
        ql.Sqrt(arr_mix)

    arr_log = ql.Array([1.0, math.e, math.e**2])
    assert approx_equal_array(ql.Log(arr_log), [0.0, 1.0, 2.0])

    arr_exp = ql.Array([0.0, 1.0, 2.0])
    assert approx_equal_array(ql.Exp(arr_exp), [1.0, math.e, math.e**2])

    arr_pow = ql.Array([1.0, 2.0, 3.0])
    assert approx_equal_array(ql.Pow(arr_pow, 2.0), [1.0, 4.0, 9.0])

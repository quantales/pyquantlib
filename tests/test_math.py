"""
Tests for math module.

Corresponds to src/math/*.cpp bindings.
"""

import math

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal

import pyquantlib as ql


def approx_equal_array(arr1, arr2):
    """Helper to compare arrays with pytest.approx."""
    if len(arr1) != len(arr2):
        return False
    for x, y in zip(arr1, arr2):
        if not x == pytest.approx(y):
            return False
    return True


# =============================================================================
# Array - Constructors
# =============================================================================


def test_array_default_constructor():
    """Test Array default constructor."""
    arr = ql.Array()
    assert isinstance(arr, ql.Array)
    assert len(arr) == 0
    assert arr.empty()


def test_array_size_constructor():
    """Test Array size constructor."""
    arr = ql.Array(5)
    assert len(arr) == 5


def test_array_size_value_constructor():
    """Test Array size and value constructor."""
    arr = ql.Array(3, 7.5)
    assert len(arr) == 3
    for i in range(3):
        assert arr[i] == 7.5


def test_array_iterable_constructor():
    """Test Array construction from iterables."""
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
    """Test Array construction from numpy array."""
    np_data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
    arr = ql.Array(np_data)
    assert len(arr) == len(np_data)
    for i in range(len(np_data)):
        assert arr[i] == np_data[i]

    with pytest.raises(RuntimeError):
        ql.Array(np.array([[1, 2], [3, 4]]))


# =============================================================================
# Array - Buffer Protocol
# =============================================================================


def test_array_to_numpy_view():
    """Test Array to numpy view (shared memory)."""
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
    """Test Array to numpy copy (independent memory)."""
    ql_arr = ql.Array([1.0, 2.0, 3.0])
    np_copy = np.array(ql_arr, copy=True)
    np_copy[0] = 99.0
    assert ql_arr[0] != 99.0


# =============================================================================
# Array - Size and Capacity
# =============================================================================


def test_array_size_len_empty():
    """Test Array size, len, and empty methods."""
    arr = ql.Array([1, 2, 3])
    assert arr.size() == 3
    assert len(arr) == 3
    assert not arr.empty()

    arr_empty = ql.Array()
    assert arr_empty.size() == 0
    assert len(arr_empty) == 0
    assert arr_empty.empty()


def test_array_resize():
    """Test Array resize method."""
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
    """Test Array swap method."""
    arr1 = ql.Array([1, 2])
    arr2 = ql.Array([3, 4, 5])

    arr1_orig = list(arr1)
    arr2_orig = list(arr2)

    arr1.swap(arr2)

    assert list(arr1) == arr2_orig
    assert list(arr2) == arr1_orig


def test_array_fill():
    """Test Array fill method."""
    arr = ql.Array(3)
    arr.fill(5.5)
    assert len(arr) == 3
    for x in arr:
        assert x == 5.5


# =============================================================================
# Array - Element Access
# =============================================================================


def test_array_getitem_setitem():
    """Test Array element access via []."""
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
    """Test Array.at method with bounds checking."""
    arr = ql.Array([1.0, 2.0])
    assert arr.at(0) == 1.0
    assert arr.at(1) == 2.0

    with pytest.raises(ql.Error):
        arr.at(2)


def test_array_front_back():
    """Test Array front and back methods."""
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


# =============================================================================
# Array - Iteration and Repr
# =============================================================================


def test_array_iteration():
    """Test Array iteration."""
    data = [1.1, 2.2, 3.3]
    arr = ql.Array(data)

    iterated = list(arr)
    assert iterated == data
    assert list(ql.Array([])) == []


def test_array_repr():
    """Test Array repr."""
    arr = ql.Array([1, 2, 3])
    assert repr(arr) == "Array([1, 2, 3])"

    arr_empty = ql.Array([])
    assert repr(arr_empty) == "Array([])"

    arr_long = ql.Array([float(i) for i in range(20)])
    assert "...," in repr(arr_long)


# =============================================================================
# Array - Operators
# =============================================================================


def test_array_unary_minus():
    """Test Array unary minus operator."""
    arr = ql.Array([1.0, -2.0, 0.0])
    neg_arr = -arr
    assert isinstance(neg_arr, ql.Array)
    assert approx_equal_array(neg_arr, [-1.0, 2.0, 0.0])
    assert approx_equal_array(arr, [1.0, -2.0, 0.0])


def test_array_inplace_operators_array():
    """Test Array in-place operators with arrays."""
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
    """Test Array in-place operators with scalars."""
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
    """Test Array binary operators with arrays."""
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([4, 5, 6])

    assert approx_equal_array(arr1 + arr2, [5, 7, 9])
    assert approx_equal_array(arr1 - arr2, [-3, -3, -3])
    assert approx_equal_array(arr1 * arr2, [4, 10, 18])
    assert approx_equal_array(ql.Array([4, 10, 18]) / ql.Array([2, 2, 3]), [2, 5, 6])


def test_array_binary_operators_scalar():
    """Test Array binary operators with scalars."""
    arr = ql.Array([1, 2, 3])

    assert approx_equal_array(arr + 2.0, [3, 4, 5])
    assert approx_equal_array(arr - 1.0, [0, 1, 2])
    assert approx_equal_array(arr * 3.0, [3, 6, 9])
    assert approx_equal_array(arr / 2.0, [0.5, 1.0, 1.5])


def test_array_reverse_scalar_operators():
    """Test Array reverse scalar operators."""
    arr = ql.Array([1, 2, 3])

    assert approx_equal_array(2.0 + arr, [3, 4, 5])
    assert approx_equal_array(5.0 - arr, [4, 3, 2])
    assert approx_equal_array(3.0 * arr, [3, 6, 9])
    assert approx_equal_array(12.0 / ql.Array([2, 4, 6]), [6.0, 3.0, 2.0])


def test_array_comparison_operators():
    """Test Array comparison operators."""
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


# =============================================================================
# Array - Math Functions
# =============================================================================


def test_array_dot_product():
    """Test DotProduct function."""
    arr1 = ql.Array([1, 2, 3])
    arr2 = ql.Array([4, 5, 6])
    assert ql.DotProduct(arr1, arr2) == pytest.approx(32.0)

    with pytest.raises(ql.Error):
        ql.DotProduct(arr1, ql.Array([1, 2]))


def test_array_unary_functions():
    """Test Array unary math functions."""
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


# =============================================================================
# Array - Implicit Conversion
# =============================================================================


def test_array_implicit_conversion_list():
    """Lists can be passed directly to functions expecting Array."""
    result = ql.DotProduct([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
    assert result == pytest.approx(32.0)


def test_array_implicit_conversion_numpy():
    """Numpy arrays can be passed directly to functions expecting Array."""
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    result = ql.DotProduct(a, b)
    assert result == pytest.approx(32.0)


def test_array_implicit_conversion_mixed():
    """Mixed list and numpy array work together."""
    result = ql.DotProduct([1.0, 2.0, 3.0], np.array([4.0, 5.0, 6.0]))
    assert result == pytest.approx(32.0)


# =============================================================================
# Matrix - Constructors
# =============================================================================


def test_matrix_default_constructor():
    """Test Matrix default constructor."""
    m = ql.Matrix()
    assert m.rows() == 0
    assert m.columns() == 0
    assert m.empty()
    assert m.shape == (0, 0)
    assert "Matrix(0, 0)" in repr(m)


def test_matrix_dimensions_constructor():
    """Test Matrix dimensions constructor."""
    m = ql.Matrix(2, 3, 0)
    assert m.rows() == 2
    assert m.columns() == 3
    assert not m.empty()
    assert m.shape == (2, 3)
    assert_array_equal(np.array(m), np.zeros((2, 3)))


def test_matrix_dimensions_value_constructor():
    """Test Matrix dimensions and value constructor."""
    m = ql.Matrix(3, 2, 7.5)
    assert m.rows() == 3
    assert m.columns() == 2
    assert not m.empty()
    assert_array_equal(np.array(m), np.full((3, 2), 7.5))


def test_matrix_numpy_constructor():
    """Test Matrix construction from numpy array."""
    np_arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.double)
    m = ql.Matrix(np_arr)
    assert m.rows() == 2
    assert m.columns() == 3
    assert_array_equal(np.array(m), np_arr)

    np_empty_cols = np.array([[]], dtype=np.double)
    m_empty_cols = ql.Matrix(np_empty_cols)
    assert m_empty_cols.rows() == 1
    assert m_empty_cols.columns() == 0
    assert m_empty_cols.empty()

    np_empty_rows = np.empty((0, 2), dtype=np.double)
    m_empty_rows = ql.Matrix(np_empty_rows)
    assert m_empty_rows.rows() == 0
    assert m_empty_rows.columns() == 2
    assert m_empty_rows.empty()


def test_matrix_numpy_wrong_dims():
    """Test Matrix rejects wrong-dimensional numpy arrays."""
    with pytest.raises(ValueError, match="Input array must be 2-dimensional"):
        ql.Matrix(np.array([1.0, 2.0, 3.0]))
    with pytest.raises(ValueError, match="Input array must be 2-dimensional"):
        ql.Matrix(np.array([[[1.0]]]))


def test_matrix_list_of_lists_constructor():
    """Test Matrix construction from list of lists."""
    lol = [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]]
    m = ql.Matrix(lol)
    assert m.rows() == 3
    assert m.columns() == 2
    assert_array_almost_equal(np.array(m), np.array(lol))

    m_empty = ql.Matrix([])
    assert m_empty.rows() == 0
    assert m_empty.columns() == 0
    assert m_empty.empty()

    m_empty_cols = ql.Matrix([[], []])
    assert m_empty_cols.rows() == 2
    assert m_empty_cols.columns() == 0
    assert m_empty_cols.empty()


def test_matrix_list_of_lists_malformed():
    """Test Matrix rejects malformed list of lists."""
    with pytest.raises(TypeError, match="Input must be a list of lists"):
        ql.Matrix([1, 2, 3])
    with pytest.raises(TypeError, match="All elements of the outer list must be lists"):
        ql.Matrix([[1, 2], 3, [4, 5]])
    with pytest.raises(ValueError, match="Inconsistent number of columns"):
        ql.Matrix([[1, 2], [3, 4, 5]])


# =============================================================================
# Matrix - Properties
# =============================================================================


def test_matrix_properties():
    """Test Matrix properties."""
    m = ql.Matrix(4, 5)
    assert m.rows() == 4
    assert m.columns() == 5
    assert m.shape == (4, 5)
    assert not m.empty()

    m_empty_rows = ql.Matrix(0, 5)
    assert m_empty_rows.rows() == 0
    assert m_empty_rows.columns() == 5
    assert m_empty_rows.shape == (0, 5)
    assert m_empty_rows.empty()

    m_empty_cols = ql.Matrix(5, 0)
    assert m_empty_cols.rows() == 5
    assert m_empty_cols.columns() == 0
    assert m_empty_cols.shape == (5, 0)
    assert m_empty_cols.empty()


# =============================================================================
# Matrix - Element Access
# =============================================================================


def test_matrix_getitem_setitem_element():
    """Test Matrix element access via [row, col]."""
    m = ql.Matrix(2, 3, 1.0)
    m[0, 0] = 1.1
    m[0, 1] = 2.2
    m[0, 2] = 3.3
    m[1, 0] = 4.4
    m[1, 1] = 5.5
    m[1, 2] = 6.6

    assert m[0, 0] == pytest.approx(1.1)
    assert m[0, 1] == pytest.approx(2.2)
    assert m[0, 2] == pytest.approx(3.3)
    assert m[1, 0] == pytest.approx(4.4)
    assert m[1, 1] == pytest.approx(5.5)
    assert m[1, 2] == pytest.approx(6.6)

    with pytest.raises(IndexError):
        _ = m[2, 0]
    with pytest.raises(IndexError):
        _ = m[0, 3]
    with pytest.raises(IndexError):
        m[2, 0] = 0.0
    with pytest.raises(IndexError):
        m[0, 3] = 0.0


def test_matrix_getitem_row_view():
    """Test Matrix row view access."""
    np_orig = np.array([[1., 2., 3.], [4., 5., 6.]])
    m = ql.Matrix(np_orig)

    row0_view = m[0]
    assert isinstance(row0_view, np.ndarray)
    assert_array_equal(row0_view, np_orig[0, :])

    row0_view[1] = 99.0
    assert m[0, 1] == pytest.approx(99.0)
    assert np_orig[0, 1] != 99.0

    m[1][2] = 101.0
    assert m[1, 2] == pytest.approx(101.0)

    with pytest.raises(IndexError):
        _ = m[2]

    m_zero_cols = ql.Matrix(2, 0)
    row_view = m_zero_cols[0]
    assert isinstance(row_view, np.ndarray)
    assert row_view.shape == (0,)


# =============================================================================
# Matrix - Iteration and Buffer Protocol
# =============================================================================


def test_matrix_iteration():
    """Test Matrix iteration."""
    m = ql.Matrix([[1.0, 2.0], [3.0, 4.0]])
    assert list(m) == [1.0, 2.0, 3.0, 4.0]
    assert list(ql.Matrix()) == []
    assert list(ql.Matrix(1, 1, 5.0)) == [5.0]


def test_matrix_buffer_protocol():
    """Test Matrix buffer protocol."""
    m_ql = ql.Matrix([[10., 20.], [30., 40.]])

    np_view = np.array(m_ql, copy=False)
    assert_array_equal(np_view, np.array([[10., 20.], [30., 40.]]))

    np_view[0, 0] = 100.0
    assert m_ql[0, 0] == pytest.approx(100.0)

    m_ql[1, 1] = 400.0
    assert np_view[1, 1] == pytest.approx(400.0)

    np_empty = np.array(ql.Matrix(0, 0), copy=False)
    assert np_empty.shape == (0, 0)

    np_empty_rows = np.array(ql.Matrix(0, 2), copy=False)
    assert np_empty_rows.shape == (0, 2)

    np_empty_cols = np.array(ql.Matrix(2, 0), copy=False)
    assert np_empty_cols.shape == (2, 0)


# =============================================================================
# Matrix - Methods
# =============================================================================


def test_matrix_swap():
    """Test Matrix swap method."""
    m1 = ql.Matrix([[1., 2.], [3., 4.]])
    m2 = ql.Matrix([[5., 6.], [7., 8.]])

    m1_orig = np.array(m1).copy()
    m2_orig = np.array(m2).copy()

    m1.swap(m2)

    assert_array_equal(np.array(m1), m2_orig)
    assert_array_equal(np.array(m2), m1_orig)


def test_matrix_diagonal():
    """Test Matrix diagonal method."""
    m = ql.Matrix([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
    assert_array_equal(np.array(m.diagonal()), [1., 5., 9.])

    m_rect = ql.Matrix([[1., 2., 3., 4.], [5., 6., 7., 8.]])
    assert_array_equal(np.array(m_rect.diagonal()), [1., 6.])

    m_rect2 = ql.Matrix([[1., 2.], [3., 4.], [5., 6.]])
    assert_array_equal(np.array(m_rect2.diagonal()), [1., 4.])

    m_empty = ql.Matrix(0, 0)
    assert len(np.array(m_empty.diagonal())) == 0


def test_matrix_column():
    """Test Matrix column method."""
    m = ql.Matrix([[1., 2., 3.], [4., 5., 6.]])

    assert_array_equal(np.array(m.column(0)), [1., 4.])
    assert_array_equal(np.array(m.column(1)), [2., 5.])
    assert_array_equal(np.array(m.column(2)), [3., 6.])

    with pytest.raises(IndexError):
        m.column(3)

    m_empty_rows = ql.Matrix(0, 3)
    assert len(np.array(m_empty_rows.column(0))) == 0


def test_matrix_transpose():
    """Test transpose function."""
    m_np = np.array([[1., 2., 3.], [4., 5., 6.]], dtype=np.double)
    m = ql.Matrix(m_np)

    transposed = ql.transpose(m)
    assert transposed.rows() == 3
    assert transposed.columns() == 2
    assert_array_equal(np.array(transposed), m_np.T)

    m_sq = ql.Matrix([[1., 2.], [3., 4.]])
    assert_array_equal(np.array(ql.transpose(m_sq)), np.array([[1., 3.], [2., 4.]]))

    m_row = ql.Matrix([[10., 20., 30.]])
    t_row = ql.transpose(m_row)
    assert t_row.rows() == 3
    assert t_row.columns() == 1

    m_col = ql.Matrix([[10.], [20.], [30.]])
    t_col = ql.transpose(m_col)
    assert t_col.rows() == 1
    assert t_col.columns() == 3

    t_empty_cols = ql.transpose(ql.Matrix(3, 0))
    assert t_empty_cols.rows() == 0
    assert t_empty_cols.columns() == 3

    t_empty_rows = ql.transpose(ql.Matrix(0, 3))
    assert t_empty_rows.rows() == 3
    assert t_empty_rows.columns() == 0


# =============================================================================
# Matrix - Operators
# =============================================================================


def test_matrix_inplace_add_sub():
    """Test Matrix in-place add and subtract."""
    m1 = ql.Matrix([[1., 2.], [3., 4.]])
    m2 = ql.Matrix([[0.5, 1.5], [2.5, 3.5]])

    m1 += m2
    assert_array_almost_equal(np.array(m1), [[1.5, 3.5], [5.5, 7.5]])

    m1 -= m2
    assert_array_almost_equal(np.array(m1), [[1., 2.], [3., 4.]])


def test_matrix_inplace_mul_div_scalar():
    """Test Matrix in-place multiply and divide by scalar."""
    m = ql.Matrix([[1., 2.], [3., 4.]])

    m *= 2.0
    assert_array_almost_equal(np.array(m), [[2., 4.], [6., 8.]])

    m /= 2.0
    assert_array_almost_equal(np.array(m), [[1., 2.], [3., 4.]])

    with pytest.raises(ValueError):
        m /= 0.0


def test_matrix_binary_add_sub():
    """Test Matrix binary add and subtract."""
    m1 = ql.Matrix([[1., 2.], [3., 4.]])
    m2 = ql.Matrix([[0.5, 1.5], [2.5, 3.5]])

    assert_array_almost_equal(np.array(m1 + m2), [[1.5, 3.5], [5.5, 7.5]])
    assert_array_almost_equal(np.array(m1 - m2), [[0.5, 0.5], [0.5, 0.5]])


def test_matrix_binary_mul_div_scalar():
    """Test Matrix binary multiply and divide by scalar."""
    m = ql.Matrix([[1., 2.], [3., 4.]])

    assert_array_almost_equal(np.array(m * 3.0), [[3., 6.], [9., 12.]])
    assert_array_almost_equal(np.array(3.0 * m), [[3., 6.], [9., 12.]])
    assert_array_almost_equal(np.array(m / 2.0), [[0.5, 1.], [1.5, 2.]])

    with pytest.raises(ValueError):
        _ = m / 0.0


def test_matrix_multiplication():
    """Test Matrix multiplication."""
    m1 = ql.Matrix([[1., 2.], [3., 4.]])
    m2 = ql.Matrix([[5., 6., 7.], [8., 9., 10.]])

    prod = m1 * m2
    expected = np.dot(np.array([[1., 2.], [3., 4.]]),
                     np.array([[5., 6., 7.], [8., 9., 10.]]))
    assert prod.rows() == 2
    assert prod.columns() == 3
    assert_array_almost_equal(np.array(prod), expected)

    m3 = ql.Matrix([[1., 1.], [1., 1.], [1., 1.]])
    with pytest.raises(ql.Error):
        _ = m1 * m3


def test_matrix_outer_product():
    """Test outerProduct function."""
    arr1 = ql.Array([1., 2., 3.])
    arr2 = ql.Array([4., 5.])

    outer = ql.outerProduct(arr1, arr2)

    assert outer.rows() == 3
    assert outer.columns() == 2
    assert_array_almost_equal(np.array(outer), np.outer([1., 2., 3.], [4., 5.]))


# =============================================================================
# Matrix - Repr
# =============================================================================


def test_matrix_repr_str():
    """Test Matrix repr and str."""
    m = ql.Matrix(2, 2, 1.23)
    assert "Matrix(2, 2)" in repr(m)
    assert "1.23" in repr(m)
    assert "Matrix(2, 2)" in str(m)
    assert "1.23" in str(m)

    m_large = ql.Matrix(20, 20, 1.0)
    assert "..." in repr(m_large)
    assert "..." in str(m_large)


# =============================================================================
# Matrix - Implicit Conversion
# =============================================================================


def test_matrix_implicit_conversion_list():
    """List of lists can be passed directly to functions expecting Matrix."""
    data = [[1., 2.], [3., 4.]]
    result = ql.transpose(data)
    assert result.rows() == 2
    assert result.columns() == 2
    assert_array_almost_equal(np.array(result), [[1., 3.], [2., 4.]])


def test_matrix_implicit_conversion_numpy():
    """Numpy arrays can be passed directly to functions expecting Matrix."""
    data = np.array([[1., 2.], [3., 4.]])
    result = ql.transpose(data)
    assert result.rows() == 2
    assert result.columns() == 2
    assert_array_almost_equal(np.array(result), [[1., 3.], [2., 4.]])


# =============================================================================
# Interpolation - Base Class
# =============================================================================


def test_interpolation_base_class_exists():
    """Test Interpolation base class is in base submodule."""
    assert hasattr(ql.base, "Interpolation")


def test_interpolation_isinstance():
    """Test concrete interpolations are instances of base Interpolation."""
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    interp = ql.LinearInterpolation(x, y)
    assert isinstance(interp, ql.base.Interpolation)


# =============================================================================
# LinearInterpolation
# =============================================================================


def test_linearinterpolation_construction():
    """Test LinearInterpolation construction."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 4.0, 9.0, 16.0]
    interp = ql.LinearInterpolation(x, y)
    assert interp is not None


def test_linearinterpolation_call():
    """Test LinearInterpolation evaluation."""
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0, 30.0]
    interp = ql.LinearInterpolation(x, y)

    # At nodes
    assert interp(1.0) == pytest.approx(10.0)
    assert interp(2.0) == pytest.approx(20.0)
    assert interp(3.0) == pytest.approx(30.0)

    # Between nodes (linear interpolation)
    assert interp(1.5) == pytest.approx(15.0)
    assert interp(2.5) == pytest.approx(25.0)


def test_linearinterpolation_xmin_xmax():
    """Test LinearInterpolation xMin and xMax methods."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 4.0, 9.0, 16.0]
    interp = ql.LinearInterpolation(x, y)

    assert interp.xMin() == pytest.approx(1.0)
    assert interp.xMax() == pytest.approx(4.0)


def test_linearinterpolation_derivative():
    """Test LinearInterpolation derivative method."""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 2.0, 4.0]  # y = 2x, derivative = 2
    interp = ql.LinearInterpolation(x, y)

    assert interp.derivative(0.5) == pytest.approx(2.0)
    assert interp.derivative(1.5) == pytest.approx(2.0)


def test_linearinterpolation_primitive():
    """Test LinearInterpolation primitive (integral) method."""
    x = [0.0, 1.0, 2.0]
    y = [1.0, 1.0, 1.0]  # constant y=1, integral from 0 to x is x
    interp = ql.LinearInterpolation(x, y)

    assert interp.primitive(0.0) == pytest.approx(0.0)
    assert interp.primitive(1.0) == pytest.approx(1.0)
    assert interp.primitive(2.0) == pytest.approx(2.0)


def test_linearinterpolation_data_lifetime():
    """Test LinearInterpolation data lifetime (no dangling pointers)."""
    def create_interp():
        x = [1.0, 2.0, 3.0]
        y = [10.0, 20.0, 30.0]
        return ql.LinearInterpolation(x, y)

    interp = create_interp()
    # Data should still be valid after local variables are gone
    assert interp(1.5) == pytest.approx(15.0)
    assert interp.xMin() == pytest.approx(1.0)
    assert interp.xMax() == pytest.approx(3.0)


def test_linearinterpolation_validation():
    """Test LinearInterpolation input validation."""
    with pytest.raises(ql.Error):
        ql.LinearInterpolation([1.0], [1.0])  # Need at least 2 points

    with pytest.raises(ql.Error):
        ql.LinearInterpolation([1.0, 2.0], [1.0])  # Size mismatch


# =============================================================================
# LogLinearInterpolation
# =============================================================================


def test_loglinearinterpolation_construction():
    """Test LogLinearInterpolation construction."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 2.0, 4.0, 8.0]
    interp = ql.LogLinearInterpolation(x, y)
    assert interp is not None


def test_loglinearinterpolation_call():
    """Test LogLinearInterpolation evaluation."""
    x = [1.0, 2.0]
    y = [1.0, math.e]  # y = e^(x-1)
    interp = ql.LogLinearInterpolation(x, y)

    assert interp(1.0) == pytest.approx(1.0)
    assert interp(2.0) == pytest.approx(math.e)
    # Log-linear interpolates in log space
    assert interp(1.5) == pytest.approx(math.exp(0.5))


def test_loglinearinterpolation_data_lifetime():
    """Test LogLinearInterpolation data lifetime."""
    def create_interp():
        x = [1.0, 2.0, 3.0]
        y = [1.0, 2.0, 4.0]
        return ql.LogLinearInterpolation(x, y)

    interp = create_interp()
    assert interp.xMin() == pytest.approx(1.0)
    assert interp.xMax() == pytest.approx(3.0)
    assert interp(1.0) == pytest.approx(1.0)


# =============================================================================
# BackwardFlatInterpolation
# =============================================================================


def test_backwardflatinterpolation_construction():
    """Test BackwardFlatInterpolation construction."""
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0, 30.0]
    interp = ql.BackwardFlatInterpolation(x, y)
    assert interp is not None


def test_backwardflatinterpolation_call():
    """Test BackwardFlatInterpolation evaluation."""
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0, 30.0]
    interp = ql.BackwardFlatInterpolation(x, y)

    # At nodes
    assert interp(1.0) == pytest.approx(10.0)
    assert interp(2.0) == pytest.approx(20.0)
    assert interp(3.0) == pytest.approx(30.0)

    # Between nodes - backward flat uses left value
    assert interp(1.5) == pytest.approx(20.0)
    assert interp(2.5) == pytest.approx(30.0)


def test_backwardflatinterpolation_single_point():
    """Test BackwardFlatInterpolation with single point."""
    x = [1.0]
    y = [10.0]
    interp = ql.BackwardFlatInterpolation(x, y)
    assert interp(1.0) == pytest.approx(10.0)


def test_backwardflatinterpolation_data_lifetime():
    """Test BackwardFlatInterpolation data lifetime."""
    def create_interp():
        x = [1.0, 2.0, 3.0]
        y = [10.0, 20.0, 30.0]
        return ql.BackwardFlatInterpolation(x, y)

    interp = create_interp()
    assert interp(1.5) == pytest.approx(20.0)


# =============================================================================
# CubicInterpolation
# =============================================================================


def test_cubicinterpolation_enums():
    """Test CubicInterpolation enums exist."""
    # DerivativeApprox
    assert hasattr(ql, "CubicDerivativeApprox")
    assert hasattr(ql.CubicDerivativeApprox, "Spline")
    assert hasattr(ql.CubicDerivativeApprox, "Kruger")
    assert hasattr(ql.CubicDerivativeApprox, "Akima")

    # BoundaryCondition
    assert hasattr(ql, "CubicBoundaryCondition")
    assert hasattr(ql.CubicBoundaryCondition, "NotAKnot")
    assert hasattr(ql.CubicBoundaryCondition, "FirstDerivative")
    assert hasattr(ql.CubicBoundaryCondition, "SecondDerivative")


def test_cubicinterpolation_construction_defaults():
    """Test CubicInterpolation construction with defaults."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 4.0, 9.0, 16.0]
    interp = ql.CubicInterpolation(x, y)
    assert interp is not None


def test_cubicinterpolation_construction_explicit():
    """Test CubicInterpolation construction with explicit parameters."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 4.0, 9.0, 16.0]
    interp = ql.CubicInterpolation(
        x, y,
        derivativeApprox=ql.CubicDerivativeApprox.Spline,
        monotonic=False,
        leftCondition=ql.CubicBoundaryCondition.SecondDerivative,
        leftConditionValue=0.0,
        rightCondition=ql.CubicBoundaryCondition.SecondDerivative,
        rightConditionValue=0.0
    )
    assert interp is not None


def test_cubicinterpolation_call():
    """Test CubicInterpolation evaluation."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 8.0, 27.0, 64.0]  # y = x^3
    interp = ql.CubicInterpolation(x, y)

    # At nodes
    assert interp(1.0) == pytest.approx(1.0)
    assert interp(2.0) == pytest.approx(8.0)
    assert interp(3.0) == pytest.approx(27.0)
    assert interp(4.0) == pytest.approx(64.0)


def test_cubicinterpolation_smooth():
    """Test CubicInterpolation produces smooth curve."""
    x = [0.0, 1.0, 2.0, 3.0]
    y = [0.0, 1.0, 4.0, 9.0]
    interp = ql.CubicInterpolation(x, y)

    # Derivative should be continuous (smooth) - test between nodes
    eps = 1e-6
    for xi in [0.5, 1.5, 2.5]:
        left = interp.derivative(xi - eps)
        right = interp.derivative(xi + eps)
        assert left == pytest.approx(right, rel=1e-3)


def test_cubicinterpolation_data_lifetime():
    """Test CubicInterpolation data lifetime."""
    def create_interp():
        x = [1.0, 2.0, 3.0, 4.0]
        y = [1.0, 4.0, 9.0, 16.0]
        return ql.CubicInterpolation(x, y)

    interp = create_interp()
    assert interp(2.0) == pytest.approx(4.0)


# =============================================================================
# CubicNaturalSpline
# =============================================================================


def test_cubicnaturalspline_construction():
    """Test CubicNaturalSpline construction."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 4.0, 9.0, 16.0]
    interp = ql.CubicNaturalSpline(x, y)
    assert interp is not None
    assert isinstance(interp, ql.base.Interpolation)


def test_cubicnaturalspline_call():
    """Test CubicNaturalSpline evaluation."""
    x = [0.0, 1.0, 2.0, 3.0]
    y = [0.0, 1.0, 4.0, 9.0]
    interp = ql.CubicNaturalSpline(x, y)

    assert interp(0.0) == pytest.approx(0.0)
    assert interp(1.0) == pytest.approx(1.0)
    assert interp(2.0) == pytest.approx(4.0)
    assert interp(3.0) == pytest.approx(9.0)


def test_cubicnaturalspline_natural_boundary():
    """Test CubicNaturalSpline has zero second derivative at boundaries."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0]
    y = [0.0, 1.0, 0.0, 1.0, 0.0]
    interp = ql.CubicNaturalSpline(x, y)

    # Natural spline: second derivative is zero at endpoints
    eps = 1e-6
    # Approximate second derivative
    d2_left = (interp.derivative(eps) - interp.derivative(0.0)) / eps
    d2_right = (interp.derivative(4.0) - interp.derivative(4.0 - eps)) / eps
    assert d2_left == pytest.approx(0.0, abs=0.1)
    assert d2_right == pytest.approx(0.0, abs=0.1)


# =============================================================================
# MonotonicCubicNaturalSpline
# =============================================================================


def test_monotoniccubicnaturalspline_construction():
    """Test MonotonicCubicNaturalSpline construction."""
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.0, 2.0, 3.0, 4.0]
    interp = ql.MonotonicCubicNaturalSpline(x, y)
    assert interp is not None
    assert isinstance(interp, ql.base.Interpolation)


def test_monotoniccubicnaturalspline_monotonicity():
    """Test MonotonicCubicNaturalSpline preserves monotonicity."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.0, 2.0, 3.0, 4.0, 5.0]  # Monotonic increasing
    interp = ql.MonotonicCubicNaturalSpline(x, y)

    # Check monotonicity between all nodes
    prev = interp(1.0)
    for xi in [1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        curr = interp(xi)
        assert curr >= prev, f"Monotonicity violated at x={xi}"
        prev = curr


def test_monotoniccubicnaturalspline_data_lifetime():
    """Test MonotonicCubicNaturalSpline data lifetime."""
    def create_interp():
        x = [1.0, 2.0, 3.0, 4.0]
        y = [1.0, 2.0, 3.0, 4.0]
        return ql.MonotonicCubicNaturalSpline(x, y)

    interp = create_interp()
    assert interp(2.5) == pytest.approx(2.5, rel=0.1)

import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import pyquantlib as ql

# Skip entire module on macOS due to boost::shared_ptr holder issues
pytestmark = pytest.mark.skipif(
    sys.platform == "darwin",
    reason="Matrix tests segfault on macOS - boost::shared_ptr holder issue"
)


class TestMatrixConstructors:

    def test_default(self):
        m = ql.Matrix()
        assert m.rows() == 0
        assert m.columns() == 0
        assert m.empty()
        assert m.shape == (0, 0)
        assert "Matrix(0, 0)" in repr(m)

    def test_dimensions(self):
        m = ql.Matrix(2, 3, 0)
        assert m.rows() == 2
        assert m.columns() == 3
        assert not m.empty()
        assert m.shape == (2, 3)
        assert_array_equal(np.array(m), np.zeros((2, 3)))

    def test_dimensions_value(self):
        m = ql.Matrix(3, 2, 7.5)
        assert m.rows() == 3
        assert m.columns() == 2
        assert not m.empty()
        assert_array_equal(np.array(m), np.full((3, 2), 7.5))

    def test_numpy(self):
        np_arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.double)
        m = ql.Matrix(np_arr)
        assert m.rows() == 2
        assert m.columns() == 3
        assert_array_equal(np.array(m), np_arr)

        # Empty numpy arrays
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

    def test_numpy_wrong_dims(self):
        with pytest.raises(ValueError, match="Input array must be 2-dimensional"):
            ql.Matrix(np.array([1.0, 2.0, 3.0]))
        with pytest.raises(ValueError, match="Input array must be 2-dimensional"):
            ql.Matrix(np.array([[[1.0]]]))

    def test_list_of_lists(self):
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

    def test_list_of_lists_malformed(self):
        with pytest.raises(TypeError, match="Input must be a list of lists"):
            ql.Matrix([1, 2, 3])
        with pytest.raises(TypeError, match="All elements of the outer list must be lists"):
            ql.Matrix([[1, 2], 3, [4, 5]])
        with pytest.raises(ValueError, match="Inconsistent number of columns"):
            ql.Matrix([[1, 2], [3, 4, 5]])


class TestMatrixProperties:

    def test_properties(self):
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


class TestMatrixElementAccess:

    def test_getitem_setitem_element(self):
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

    def test_getitem_row_view(self):
        np_orig = np.array([[1., 2., 3.], [4., 5., 6.]])
        m = ql.Matrix(np_orig)

        row0_view = m[0]
        assert isinstance(row0_view, np.ndarray)
        assert_array_equal(row0_view, np_orig[0, :])

        # Modify view affects matrix
        row0_view[1] = 99.0
        assert m[0, 1] == pytest.approx(99.0)
        assert np_orig[0, 1] != 99.0

        # Modify via matrix[i][j]
        m[1][2] = 101.0
        assert m[1, 2] == pytest.approx(101.0)

        with pytest.raises(IndexError):
            _ = m[2]

        # Zero-column matrix
        m_zero_cols = ql.Matrix(2, 0)
        row_view = m_zero_cols[0]
        assert isinstance(row_view, np.ndarray)
        assert row_view.shape == (0,)


class TestMatrixIteration:

    def test_iteration(self):
        m = ql.Matrix([[1.0, 2.0], [3.0, 4.0]])
        assert list(m) == [1.0, 2.0, 3.0, 4.0]
        assert list(ql.Matrix()) == []
        assert list(ql.Matrix(1, 1, 5.0)) == [5.0]


class TestMatrixBufferProtocol:

    def test_buffer_protocol(self):
        m_ql = ql.Matrix([[10., 20.], [30., 40.]])

        np_view = np.array(m_ql, copy=False)
        assert_array_equal(np_view, np.array([[10., 20.], [30., 40.]]))

        np_view[0, 0] = 100.0
        assert m_ql[0, 0] == pytest.approx(100.0)

        m_ql[1, 1] = 400.0
        assert np_view[1, 1] == pytest.approx(400.0)

        # Empty matrices
        np_empty = np.array(ql.Matrix(0, 0), copy=False)
        assert np_empty.shape == (0, 0)

        np_empty_rows = np.array(ql.Matrix(0, 2), copy=False)
        assert np_empty_rows.shape == (0, 2)

        np_empty_cols = np.array(ql.Matrix(2, 0), copy=False)
        assert np_empty_cols.shape == (2, 0)


class TestMatrixMethods:

    def test_swap(self):
        m1 = ql.Matrix([[1., 2.], [3., 4.]])
        m2 = ql.Matrix([[5., 6.], [7., 8.]])

        m1_orig = np.array(m1).copy()
        m2_orig = np.array(m2).copy()

        m1.swap(m2)

        assert_array_equal(np.array(m1), m2_orig)
        assert_array_equal(np.array(m2), m1_orig)

    def test_diagonal(self):
        m = ql.Matrix([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        assert_array_equal(np.array(m.diagonal()), [1., 5., 9.])

        m_rect = ql.Matrix([[1., 2., 3., 4.], [5., 6., 7., 8.]])
        assert_array_equal(np.array(m_rect.diagonal()), [1., 6.])

        m_rect2 = ql.Matrix([[1., 2.], [3., 4.], [5., 6.]])
        assert_array_equal(np.array(m_rect2.diagonal()), [1., 4.])

        m_empty = ql.Matrix(0, 0)
        assert len(np.array(m_empty.diagonal())) == 0

    def test_column(self):
        m = ql.Matrix([[1., 2., 3.], [4., 5., 6.]])

        assert_array_equal(np.array(m.column(0)), [1., 4.])
        assert_array_equal(np.array(m.column(1)), [2., 5.])
        assert_array_equal(np.array(m.column(2)), [3., 6.])

        with pytest.raises(IndexError):
            m.column(3)

        m_empty_rows = ql.Matrix(0, 3)
        assert len(np.array(m_empty_rows.column(0))) == 0

    def test_transpose(self):
        m_np = np.array([[1., 2., 3.], [4., 5., 6.]], dtype=np.double)
        m = ql.Matrix(m_np)

        transposed = ql.transpose(m)
        assert transposed.rows() == 3
        assert transposed.columns() == 2
        assert_array_equal(np.array(transposed), m_np.T)

        # Square
        m_sq = ql.Matrix([[1., 2.], [3., 4.]])
        assert_array_equal(np.array(ql.transpose(m_sq)), np.array([[1., 3.], [2., 4.]]))

        # Row vector
        m_row = ql.Matrix([[10., 20., 30.]])
        t_row = ql.transpose(m_row)
        assert t_row.rows() == 3
        assert t_row.columns() == 1

        # Column vector
        m_col = ql.Matrix([[10.], [20.], [30.]])
        t_col = ql.transpose(m_col)
        assert t_col.rows() == 1
        assert t_col.columns() == 3

        # Empty matrices
        t_empty_cols = ql.transpose(ql.Matrix(3, 0))
        assert t_empty_cols.rows() == 0
        assert t_empty_cols.columns() == 3

        t_empty_rows = ql.transpose(ql.Matrix(0, 3))
        assert t_empty_rows.rows() == 3
        assert t_empty_rows.columns() == 0


class TestMatrixOperators:

    def test_inplace_add_sub(self):
        m1 = ql.Matrix([[1., 2.], [3., 4.]])
        m2 = ql.Matrix([[0.5, 1.5], [2.5, 3.5]])

        m1 += m2
        assert_array_almost_equal(np.array(m1), [[1.5, 3.5], [5.5, 7.5]])

        m1 -= m2
        assert_array_almost_equal(np.array(m1), [[1., 2.], [3., 4.]])

    def test_inplace_mul_div_scalar(self):
        m = ql.Matrix([[1., 2.], [3., 4.]])

        m *= 2.0
        assert_array_almost_equal(np.array(m), [[2., 4.], [6., 8.]])

        m /= 2.0
        assert_array_almost_equal(np.array(m), [[1., 2.], [3., 4.]])

        with pytest.raises(ValueError):
            m /= 0.0

    def test_binary_add_sub(self):
        m1 = ql.Matrix([[1., 2.], [3., 4.]])
        m2 = ql.Matrix([[0.5, 1.5], [2.5, 3.5]])

        assert_array_almost_equal(np.array(m1 + m2), [[1.5, 3.5], [5.5, 7.5]])
        assert_array_almost_equal(np.array(m1 - m2), [[0.5, 0.5], [0.5, 0.5]])

    def test_binary_mul_div_scalar(self):
        m = ql.Matrix([[1., 2.], [3., 4.]])

        assert_array_almost_equal(np.array(m * 3.0), [[3., 6.], [9., 12.]])
        assert_array_almost_equal(np.array(3.0 * m), [[3., 6.], [9., 12.]])
        assert_array_almost_equal(np.array(m / 2.0), [[0.5, 1.], [1.5, 2.]])

        with pytest.raises(ValueError):
            _ = m / 0.0

    def test_matrix_multiplication(self):
        m1 = ql.Matrix([[1., 2.], [3., 4.]])
        m2 = ql.Matrix([[5., 6., 7.], [8., 9., 10.]])

        prod = m1 * m2
        expected = np.dot(np.array([[1., 2.], [3., 4.]]),
                         np.array([[5., 6., 7.], [8., 9., 10.]]))
        assert prod.rows() == 2
        assert prod.columns() == 3
        assert_array_almost_equal(np.array(prod), expected)

        # Incompatible dimensions
        m3 = ql.Matrix([[1., 1.], [1., 1.], [1., 1.]])
        with pytest.raises(ql.Error):
            _ = m1 * m3


class TestMatrixOuterProduct:

    def test_outer_product(self):
        arr1 = ql.Array([1., 2., 3.])
        arr2 = ql.Array([4., 5.])

        outer = ql.outerProduct(arr1, arr2)

        assert outer.rows() == 3
        assert outer.columns() == 2
        assert_array_almost_equal(np.array(outer), np.outer([1., 2., 3.], [4., 5.]))


class TestMatrixRepr:

    def test_repr_str(self):
        m = ql.Matrix(2, 2, 1.23)
        assert "Matrix(2, 2)" in repr(m)
        assert "1.23" in repr(m)
        assert "Matrix(2, 2)" in str(m)
        assert "1.23" in str(m)

        m_large = ql.Matrix(20, 20, 1.0)
        assert "..." in repr(m_large)
        assert "..." in str(m_large)

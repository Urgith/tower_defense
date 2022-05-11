cimport numpy as np
cimport cython


ctypedef np.int_t DTYPE_t

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef int collidelist(int left, int top, int bottom, int right, np.ndarray[DTYPE_t, ndim=2] rect):
    cdef Py_ssize_t rows = rect.shape[0]
    cdef Py_ssize_t row = 0

    for row in range(rows):

        if left < rect[row, 3]:
            if right > rect[row, 0]:
                if top < rect[row, 2]:
                    if bottom > rect[row, 1]:
                        return row

    return -1

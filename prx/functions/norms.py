# ----------------------------------------------------------------------------
# Copyright (c) 2014-2016, 'prx' developers (see AUTHORS file)
# All rights reserved.
#
# Distributed under the terms of the MIT license.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------
"""Function classes for norm and norm ball indicator functions."""

from __future__ import division

import numpy as np

from . import base as _base
from ..fun import norms as _norm_fun
from ..grad import norms as _norm_grad
from ..prox import norms as _norm_prox
from ..prox import projections as _proj

__all__ = (
    'L1Norm', 'L1L2Norm', 'L2Norm', 'L2NormSqHalf', 'LInfNorm',
    'L1BallInd', 'L2BallInd', 'LInfBallInd',
)


class L1Norm(_base.NormFunction):
    """Function class for the l1-norm, ``sum(abs(x))``.

    {function_summary}


    Attributes
    ----------
    {function_attributes}


    See Also
    --------
    .NormFunction : Parent class.
    L1L2Norm : Combined l1- and l2-norm Function.
    prx.fun.norms.l1norm : Associated function.
    prx.prox.norms.prox_l1 : Prox operator function.


    Notes
    -----
    ``fun(x) = sum(abs(x))``

    {function_notes}

    The prox operator is soft thresholding::

        st(v[k], l) = {{ v[k] - l*v[k]/abs(v[k])  if abs(v[k]) > l
                      {{           0              otherwise

    """

    @property
    def _conjugate_class(self):
        return LInfBallInd
    fun = staticmethod(_norm_fun.l1norm)
    prox = staticmethod(_norm_prox.prox_l1)


class L1L2Norm(_base.NormFunction):
    """Function class for the combined l1- and l2-norm.

    {function_summary}


    Attributes
    ----------
    {function_attributes}


    See Also
    --------
    .NormFunction : Parent class.
    L1Norm : l1-norm Function.
    L2Norm : l2-norm Function.
    prx.fun.norms.l1l2norm : Associated function.
    prx.prox.norms.prox_l1l2 : Prox operator function.


    Notes
    -----
    ``fun(x) = l1norm(l2norm(x, axis))``

    {function_notes}

    The prox operator is block soft thresholding::

        bst(v[k, :], l) =
         {{ v[k, :] - l*v[k, :]/l2norm(v[k, :])  if l2norm(v[k, :]) > l
         {{                 0                    otherwise

    """

    def __init__(
        self, axis=-1, scale=None, stretch=None, shift=None, linear=None,
        const=None,
    ):
        """Create Function object that defines a norm function.

        {init_summary}


        Parameters
        ----------
        axis : int | tuple of ints, optional
            Axis or axes over which to calculate the l2-norm. The prox
            operator is applied over all remaining axes.
        {init_params}

        """
        self._axis = axis

        super(L1L2Norm, self).__init__(
            scale=scale, stretch=stretch, shift=shift,
            linear=linear, const=const)

    @property
    def axis(self):
        """Axis over which the l2-norm is calculated."""
        return self._axis

    def fun(self, x):
        """Combined l1- and l2-norm with l2-norm taken over axis=self.axis."""
        return _norm_fun.l1l2norm(x, self._axis)

    def prox(self, x, lmbda=1):
        """Prox op of combined l1- and l2-norm (l2 over axis=self.axis)."""
        return _norm_prox.prox_l1l2(x, lmbda=lmbda, axis=self._axis)


class L2Norm(_base.NormFunction):
    """Function class for the l2-norm, ``sqrt(sum(abs(x)**2))``.

    {function_summary}


    Attributes
    ----------
    {function_attributes}


    See Also
    --------
    .NormFunction : Parent class.
    L1L2Norm : Combined l1- and l2-norm Function.
    prx.fun.norms.l2norm : Associated function.
    prx.prox.norms.prox_l2 : Prox operator function.


    Notes
    -----
    ``fun(x) = sqrt(sum(abs(x)**2))``

    {function_notes}

    The prox operator is block soft thresholding for block=(all of v)::

        bst(v, l) = {{ v - l*v/l2norm(v)  if l2norm(v) > l
                    {{       0            otherwise

    """

    @property
    def _conjugate_class(self):
        return L2BallInd
    fun = staticmethod(_norm_fun.l2norm)
    prox = staticmethod(_norm_prox.prox_l2)


class L2NormSqHalf(_base.NormSqFunction):
    """Function class for half the squared l2-norm, 0.5*sum(abs(x)**2)).

    {function_summary}


    Attributes
    ----------
    {function_attributes}


    See Also
    --------
    .NormSqFunction : Parent class.
    L2Norm : l2-norm Function.
    prx.fun.norms.l2normsqhalf : Associated function.
    prx.grad.norms.grad_l2sqhalf : Gradient function.
    prx.prox.norms.prox_l2sqhalf : Prox operator function.


    Notes
    -----
    ``fun(x) = 0.5*sum(abs(x)**2))``

    {function_notes}

    The prox operator is the shrinkage function::

        shrink(v, l) = v/(1 + l)

    """

    @property
    def _conjugate_class(self):
        return L2NormSqHalf
    fun = staticmethod(_norm_fun.l2normsqhalf)
    grad = staticmethod(_norm_grad.grad_l2sqhalf)
    prox = staticmethod(_norm_prox.prox_l2sqhalf)


class LInfNorm(_base.NormFunction):
    """Function class for the linf-norm, ``max(abs(x))``.

    {function_summary}


    Attributes
    ----------
    {function_attributes}


    See Also
    --------
    .NormFunction : Parent class.
    prx.fun.norms.linfnorm : Associated function.
    prx.prox.norms.prox_linf : Prox operator function.


    Notes
    -----
    ``fun(x) = max(abs(x))``

    {function_notes}

    The prox operator is the peak shrinkage function, which minimizes the
    maximum value for a reduction of lmbda in the l1-norm.

    """

    @property
    def _conjugate_class(self):
        return L1BallInd
    fun = staticmethod(_norm_fun.linfnorm)
    prox = staticmethod(_norm_prox.prox_linf)


class L1BallInd(_base.NormBallFunction):
    """Function class for the indicator of the l1-ball.

    {function_summary}


    Attributes
    ----------
    radius : float | int
        Radius of the l1-ball indicator.
    {function_attributes}


    See Also
    --------
    .NormBallFunction : Parent class.
    prx.fun.norms.l1norm : l1-norm function.
    prx.prox.projections.proj_l1 : Prox operator projection function.


    Notes
    -----
    The indicator function is zero for vectors inside the ball, infinity
    for vectors outside the ball.

    {function_notes}

    The prox operator is Euclidean projection onto the l1-ball.

    """

    @property
    def _conjugate_class(self):
        return LInfNorm

    def fun(self, x):
        """Indicator function for the l1-ball with radius=self.radius."""
        nrm = _norm_fun.l1norm(x)
        eps = np.finfo(nrm.dtype).eps
        rad = self.radius
        if nrm <= rad*(1 + 10*eps):
            return 0
        else:
            return np.inf

    def prox(self, x, lmbda=1):
        """Projection onto the l1-ball with radius=self.radius."""
        return _proj.proj_l1(x, radius=self.radius)


class L2BallInd(_base.NormBallFunction):
    """Function class for the indicator of the l2-ball.

    {function_summary}


    Attributes
    ----------
    radius : float | int
        Radius of the l2-ball indicator.
    {function_attributes}


    See Also
    --------
    .NormBallFunction : Parent class.
    prx.fun.norms.l2norm : l2-norm function.
    prx.prox.projections.proj_l2 : Prox operator projection function.


    Notes
    -----
    The indicator function is zero for vectors inside the ball, infinity
    for vectors outside the ball.

    {function_notes}

    The prox operator is Euclidean projection onto the l2-ball.

    """

    @property
    def _conjugate_class(self):
        return L2Norm

    def fun(self, x):
        """Indicator function for the l2-ball with radius=self.radius."""
        nrm = _norm_fun.l2norm(x)
        eps = np.finfo(nrm.dtype).eps
        rad = self.radius
        if nrm <= rad*(1 + 10*eps):
            return 0
        else:
            return np.inf

    def prox(self, x, lmbda=1):
        """Projection onto the l2-ball with radius=self.radius."""
        return _proj.proj_l2(x, radius=self.radius)


class LInfBallInd(_base.NormBallFunction):
    """Function class for the indicator of the linf-ball.

    {function_summary}


    Attributes
    ----------
    radius : float | int
        Radius of the linf-ball indicator.
    {function_attributes}


    See Also
    --------
    .NormBallFunction : Parent class.
    prx.fun.norms.linfnorm : linf-norm function.
    prx.prox.projections.proj_linf : Prox operator projection function.


    Notes
    -----
    The indicator function is zero for vectors inside the ball, infinity
    for vectors outside the ball.

    {function_notes}

    The prox operator is Euclidean projection onto the linf-ball.

    """

    @property
    def _conjugate_class(self):
        return L1Norm

    def fun(self, x):
        """Indicator function for the linf-ball with radius=self.radius."""
        nrm = _norm_fun.linfnorm(x)
        eps = np.finfo(nrm.dtype).eps
        rad = self.radius
        if nrm <= rad*(1 + 10*eps):
            return 0
        else:
            return np.inf

    def prox(self, x, lmbda=1):
        """Projection onto the linf-ball with radius=self.radius."""
        return _proj.proj_linf(x, radius=self.radius)

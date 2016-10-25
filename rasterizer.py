# -*- coding: utf-8 -*-
import geometry
import math
import sys
#assume bottom left is the 2D origin, right is positive x direction,and up is positive y direction
ERROR_TERM_INT_FACTOR = 1

class DrivingAxis(object):
	POSITIVE_X = 1
	NEGATIVE_X = 2
	POSITIVE_Y = 3
	NEGATIVE_Y = 4

def determineDrivingAxis(start, end):
	if abs(start.x - end.x) < geometry.EPSILON:
		if end.y >= start.y:
			return DrivingAxis.POSITIVE_Y
		else:
			return DrivingAxis.NEGATIVE_Y
	else:
		absSlope = abs((end.y -start.y) / (end.x - start.x))
		if absSlope > 1.0:
			if end.y > start.y:
				return DrivingAxis.POSITIVE_Y
			else:
				return DrivingAxis.NEGATIVE_Y
		else:
			if end.x > start.x:
				return DrivingAxis.POSITIVE_X
			else:
				return DrivingAxis.NEGATIVE_X

def Bresenham_drawVertical(start, end, dc, tracePath=False):
	path = []
	startPos = start.toTuple()
	endPos = end.toTuple() 
	if abs(start.y - end.y) < geometry.EPSILON:
		x, y = int(start.x), int(start.y)
		dc.drawPoint((x, y))
		if tracePath:
			path.append((x, y))
		return path
	x = int(startPos[0])
	step = 1 if start.y < end.y else -1
	startY = int(start.y)
	endY = int(end.y) + step
	for i in xrange(startY, endY, step):
		dc.drawPoint((x, i))
		if tracePath:
			path.append((x, i))

	return path

def Bresenham_drawHorizontal(start, end, dc, tracePath=False):
	path = []
	startPos = start.toTuple()
	endPos = end.toTuple()
	if abs(start.x - end.x) < geometry.EPSILON:
		x, y = int(start.x), int(start.y)
		dc.drawPoint((x, y))
		if tracePath:
			path.append((x, y))
		return path
	y = int(startPos[1])
	step = 1 if end.x > start.x else -1
	startX = int(start.x)
	endX = int(end.x) + step
	for i in xrange(startX, endX, step):
		dc.drawPoint((i, y))
		if tracePath:
			path.append((i, y))

	return path

def Bresenham_Float_getInitialError(start, end, drivingAxis, slope):
	relativeOrigin = geometry.Vector2D(int(start.x), int(start.y))
	if drivingAxis == DrivingAxis.POSITIVE_X:
		if end.y > start.y:	#right up
			return start.y - relativeOrigin.y + (1.0 - (start.x - relativeOrigin.x)) * slope - 1.0
		else:				#right down
			return relativeOrigin.y - start.y - (1.0 - start.x + relativeOrigin.x) * slope
	elif drivingAxis == DrivingAxis.NEGATIVE_X:
		if end.y > start.y:	#left up
			return start.y - relativeOrigin.y - (start.x - relativeOrigin.x) * slope - 1.0
		else:				#left down
			return relativeOrigin.y - start.y + (start.x - relativeOrigin.x) * slope
	elif drivingAxis == DrivingAxis.POSITIVE_Y:
		if end.x > start.x:	#up right
			return start.x - relativeOrigin.x + (relativeOrigin.y + 1.0 - start.y) / slope - 1.0
		else:			#up left
			return relativeOrigin.x - start.x - (relativeOrigin.y + 1.0 - start.y) / slope
	elif drivingAxis == DrivingAxis.NEGATIVE_Y:
		if end.x > start.x:		#down right
			return start.x - relativeOrigin.x - (start.y - relativeOrigin.y) / slope - 1.0
		else:				#down left
			return relativeOrigin.x - start.x + (start.y - relativeOrigin.y) / slope

def Bresenham_Integer_getInitialError(start, end, drivingAxis, deltaX, deltaY):
	relativeOrigin = geometry.Vector2D(int(start.x), int(start.y))
	if drivingAxis == DrivingAxis.POSITIVE_X:
		if end.y > start.y:	#right up
			return int((deltaX * (start.y - relativeOrigin.y - 1.0) + (1.0 - start.x + relativeOrigin.x) * deltaY) * ERROR_TERM_INT_FACTOR)
		else:
			return int((deltaX * (relativeOrigin.y - start.y) - (1.0 - start.x + relativeOrigin.x) * deltaY) * ERROR_TERM_INT_FACTOR)
	elif drivingAxis == DrivingAxis.NEGATIVE_X:
		if end.y > start.y:	#left up
			return int((deltaX * (start.y - relativeOrigin.y - 1.0) - (start.x - relativeOrigin.x) * deltaY) * ERROR_TERM_INT_FACTOR)
		else:				#left down
			return int((deltaX * (relativeOrigin.y - start.y) + (start.x - relativeOrigin.x) * deltaY) * ERROR_TERM_INT_FACTOR)
	elif drivingAxis == DrivingAxis.POSITIVE_Y:
		if end.x > start.x:	#up right
			return int((deltaY * (start.x - relativeOrigin.x - 1.0) + (relativeOrigin.y + 1.0 - start.y) * deltaX) * ERROR_TERM_INT_FACTOR)
		else:			#up left
			return int((deltaY * (relativeOrigin.x - start.x) - (relativeOrigin.y + 1.0 - start.y) * deltaX) * ERROR_TERM_INT_FACTOR)
	elif drivingAxis == DrivingAxis.NEGATIVE_Y:
		if end.x > start.x:		#down right
			return int((deltaY * (start.x - relativeOrigin.x - 1.0) - (start.y - relativeOrigin.y) * deltaX) * ERROR_TERM_INT_FACTOR)
		else:				#down left
			return int((deltaY * (relativeOrigin.x - start.x) + (start.y - relativeOrigin.y) * deltaX) * ERROR_TERM_INT_FACTOR)

def Bresenham_Integer(start, end, dc, tracePath=False):
	path = []
	drivingAxis = determineDrivingAxis(start, end)
	if abs(start.x - end.x) < geometry.EPSILON:
		path = Bresenham_drawVertical(start, end, dc, tracePath)
		return path
	if abs(start.y - end.y) < geometry.EPSILON:
		path = Bresenham_drawHorizontal(start, end, dc, tracePath)
		return path


	deltaX = end.x - start.x
	deltaY = end.y - start.y
	errorTerm = Bresenham_Integer_getInitialError(start, end, drivingAxis, deltaX, deltaY)
	x = int(start.x)
	y = int(start.y)
	errorTermStepX = abs(ERROR_TERM_INT_FACTOR * deltaX)
	errorTermStepY = abs(deltaY * ERROR_TERM_INT_FACTOR)
	yStep = 1 if end.y > start.y else -1
	xStep = 1 if end.x > start.x else -1
	if drivingAxis in(DrivingAxis.POSITIVE_X, DrivingAxis.NEGATIVE_X):
		for x in xrange(int(math.floor(start.x)), int(math.ceil(end.x)), xStep):
			dc.drawPoint((x, y))
			if tracePath:
				path.append((x, y))
			if errorTerm >= 0:
				errorTerm -= errorTermStepX
				y += yStep
			errorTerm += errorTermStepY
	else:
		for y in xrange(int(math.floor(start.y)), int(math.ceil(end.y)), yStep):
			dc.drawPoint((x, y))
			if tracePath:
				path.append((x, y))
			if errorTerm >= 0:
				errorTerm -= errorTermStepY
				x += xStep
			errorTerm += errorTermStepX

	return path

def Bresenham_Triangle(vertices, dc, fill=True):
	path1 = Bresenham_Integer(vertices[0], vertices[2], dc, tracePath=fill)
	path2 = Bresenham_Integer(vertices[0], vertices[1], dc, tracePath=fill)
	path3 = Bresenham_Integer(vertices[1], vertices[2], dc, tracePath=fill)
	leftEndpoints = []
	rightEndpoints = []
	for x, y in path1:
		if not leftEndpoints:
			leftEndpoints.append((x, y))
		elif y < leftEndpoints[len(leftEndpoints)- 1][1]:
			leftEndpoints.append((x, y))

	for x, y in path2:
		if not rightEndpoints:
			rightEndpoints.append((x, y))
		elif y < rightEndpoints[len(rightEndpoints) - 1][1]:
			rightEndpoints.append((x, y))

	for x, y in path3:
		if not rightEndpoints:
			rightEndpoints.append((x, y))
		elif y < rightEndpoints[len(rightEndpoints) - 1][1]:
			rightEndpoints.append((x, y))
	# print 'len(leftEndpoints)', len(leftEndpoints)
	# print 'len(rightEndpoints)', len(rightEndpoints)
	# l1 = map(lambda x : x[1], leftEndpoints)
	# l2 = map(lambda x : x[1], rightEndpoints)
	# l = set(l1) - set(l2)
	# print 'there is an element in l1 not in l2:', l

	for (x0, y0), (x1, y1) in zip(leftEndpoints, rightEndpoints):
		start = geometry.Vector2D(x0, y0)
		end = geometry.Vector2D(x1, y1)
		Bresenham_drawHorizontal(start, end, dc)

def Bresenham_Float(start, end, dc, tracePath=False):
	path = []
	drivingAxis = determineDrivingAxis(start, end)
	if abs(start.x - end.x) < geometry.EPSILON:
		path = Bresenham_drawVertical(start, end, dc, tracePath)
		return path
	else:
		slope = (end.y - start.y) / (end.x - start.x)

	errorTerm = Bresenham_Float_getInitialError(start, end, drivingAxis, slope)
	x = int(start.x)
	y = int(start.y)
	yStep = 1 if end.y > start.y else -1
	xStep = 1 if end.x > start.x else -1
	if drivingAxis in(DrivingAxis.POSITIVE_X, DrivingAxis.NEGATIVE_X):
		for x in xrange(int(math.floor(start.x)), int(math.ceil(end.x)), xStep):
			dc.drawPoint((x, y))
			if tracePath:
				path.append((x, y))
			if errorTerm >= 0.0:
				errorTerm -= 1.0
				y += yStep
			errorTerm += abs(slope)
	else:
		for y in xrange(int(math.floor(start.y)), int(math.ceil(end.y)), yStep):
			dc.drawPoint((x, y))
			if tracePath:
				path.append((x, y))
			if errorTerm >= 0.0:
				errorTerm -= 1.0
				x += xStep
			errorTerm += abs(1.0 / slope)

	return path

def getVerticesAABB(vertices):
	xMin = yMin = sys.maxint
	xMax = yMax = 0
	for vertex in vertices:
		if vertex.position.x < xMin:
			xMin = vertex.position.x
		if vertex.position.x > xMax:
			xMax = vertex.position.x

		if vertex.position.y < yMin:
			yMin = vertex.position.y
		if vertex.position.y > yMax:
			yMax = vertex.position.y
	return (int(math.ceil(xMin)), int(math.ceil(yMin)), int(math.ceil(xMax)), int(math.ceil(yMax)))

def evaluateEdge(v0, v1, point):
	return (point.x - v0.x) * (v1.y - v0.y) - (point.y - v0.y) * (v1.x - v0.x)

def isTopleftEdge(v0, v1):
	if v0.y == v1.y and v1.x <= v0.x:
		return True

	direction = v1 - v0
	if direction.x <= 0 and direction.y <= 0:
		return True
	return False

def getColor(w0, w1, w2, area, vertices):
	ratio0 = abs(w0 / area)
	ratio1 = abs(w1 / area)
	ratio2 = abs(w2 / area)
	r = ratio0 * vertices[0].color[0] + ratio1 * vertices[1].color[0] + ratio2 * vertices[2].color[0]
	g = ratio0 * vertices[0].color[1] + ratio1 * vertices[1].color[1] + ratio2 * vertices[2].color[1]
	b = ratio0 * vertices[0].color[2] + ratio1 * vertices[1].color[2] + ratio2 * vertices[2].color[2]
	return (r, g, b)

def EdgeFunction_Triangle_Divide(vertices, dc, bounds):
	topleft01 = isTopleftEdge(vertices[0].position, vertices[1].position)
	topleft12 = isTopleftEdge(vertices[1].position, vertices[2].position)
	topleft20 = isTopleftEdge(vertices[2].position, vertices[0].position)
	area = evaluateEdge(vertices[0].position, vertices[1].position, vertices[2].position)
	for x in xrange(bounds[0], bounds[1]):
		for y in xrange(bounds[2], bounds[3]):
			point = geometry.Vector2D(x, y)
			w0 = evaluateEdge(vertices[1].position, vertices[2].position, point)
			if w0 > 0:
				continue
			w1 = evaluateEdge(vertices[2].position, vertices[0].position, point)
			if w1 > 0:
				continue
			w2 = evaluateEdge(vertices[0].position, vertices[1].position, point)
			if w2 > 0:
				continue
			onEdge12 = w0 >= -2
			onEdge20 = w1 >= -2
			onEdge01 = w2 >= -2
			if onEdge01 and not topleft01:
				continue
			if onEdge12 and not topleft12:
				continue
			if onEdge20 and not topleft20:
				continue
			color = getColor(w0, w1, w2, area, vertices)
			dc.drawPoint((x, y), color)

def EdgeFunction_Triangle(vertices, dc, fill=True):
	# import thread
	xMin, yMin, xMax, yMax = getVerticesAABB(vertices)
	# import multiprocessing
	# threadCount = multiprocessing.cpu_count()
	# if threadCount == 1:
	bounds = (xMin, xMax+1, yMin, yMax+1)
	EdgeFunction_Triangle_Divide(vertices, dc, bounds)
	# elif 2 <= threadCount <= 3:
		# bounds0 = (xMin, xMax / 2, yMin, yMax + 1)
		# bounds1 = (xMax / 2 + 1, xMax + 1, yMin, yMax + 1)
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds0), ())
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds1), ())
	# elif threadCount >= 4:
		# bounds0 = (xMin, xMax / 2, yMin, yMax / 2)
		# bounds1 = (xMax / 2 + 1, xMax + 1, yMin, yMax / 2)
		# bounds2 = (xMin, xMax / 2, yMax / 2 + 1, yMax + 1)
		# bounds3 = (xMax / 2 + 1, xMax + 1, yMax / 2 + 1, yMax + 1)
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds0), ())
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds1), ())
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds2), ())
		# thread.start_new_thread(lambda : EdgeFunction_Triangle_Divide(vertices, dc, bounds3), ())


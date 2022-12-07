package cse512

object HotzoneUtils {

  def ST_Contains(queryRectangle: String, pointString: String ): Boolean = {
    if (queryRectangle == null || queryRectangle.isEmpty || pointString == null || pointString.isEmpty)
      return false

    val rectangleCoOrds = queryRectangle.split(",")
    val x1 = rectangleCoOrds(0).toDouble
    val y1 = rectangleCoOrds(1).toDouble
    val x2 = rectangleCoOrds(2).toDouble
    val y2 = rectangleCoOrds(3).toDouble

    val pointCoOrds = pointString.split(",")
    val x = pointCoOrds(0).toDouble
    val y = pointCoOrds(1).toDouble

    if (x >= x1 && x <= x2 && y >= y1 && y <= y2)
      return true
    else if (x >= x2 && x <= x1 && y >= y2 && y <= y1)
      return true
    else
      return false // YOU NEED TO CHANGE THIS PART
  }
}

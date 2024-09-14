using System;
using System.Collections.Generic;
using System.Diagnostics;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;

namespace P5CCG;

public partial class Persona5QuadrilateralBackground : UserControl
{
    public Persona5QuadrilateralBackground()
    {
        InitializeComponent();
    }

    public void UpdateShape(int width, int height, int xDelta, int yDelta, List<double> margin)
    {
        double left = margin[0];
        double top = margin.Count > 1 ? margin[1] : left;
        double right = margin.Count > 2 ? margin[2] : left;
        double bottom = margin.Count > 2 ? margin[3] : top;

        Padding = new Thickness(left, top, right, bottom);

        var xMax = (int)(width - left - right);
        var yMax = (int)(height - top - bottom);

        Random random = new();
        var topLeftX = random.Next(xDelta);
        var topLeftY = random.Next(yDelta);
        var topRightX = random.Next(xMax - xDelta, xMax);
        var topRightY = random.Next(yDelta);
        var bottomLeftX = random.Next(xDelta);
        var bottomLeftY = random.Next(yMax - yDelta, yMax);
        var bottomRightX = random.Next(xMax - xDelta, xMax);
        var bottomRightY = random.Next(yMax - yDelta, yMax);

        var pathData =
            $"M{topLeftX},{topLeftY} L{topRightX},{topRightY} L{bottomRightX},{bottomRightY} L{bottomLeftX},{bottomLeftY} Z";

        QuadrilateralPath.Data = Geometry.Parse(pathData);
    }

    public void UpdateColor(Color color)
    {
        QuadrilateralPath.Fill = new SolidColorBrush(color);
    }

    public void UpdateStroke(Color color, int width)
    {
        QuadrilateralPath.Stroke = new SolidColorBrush(color);
        QuadrilateralPath.StrokeThickness = width;
    }
}
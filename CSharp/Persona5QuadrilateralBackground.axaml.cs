using System;
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

    public void UpdateShape(int width, int height, int xDelta, int yDelta, int margin)
    {
        Padding = new Thickness(margin);

        var xMax = width - 2 * margin;
        var yMax = height - 2 * margin;

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
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Interactivity;

namespace P5CCG
{
    public partial class Persona5StyledTextBox : UserControl
    {
        public static readonly StyledProperty<string> TextProperty =
            AvaloniaProperty.Register<Persona5StyledTextBox, string>(nameof(Text));

        public static readonly StyledProperty<string> WatermarkProperty =
            AvaloniaProperty.Register<Persona5StyledTextBox, string>(nameof(Watermark));

        public string Watermark
        {
            get => GetValue(WatermarkProperty);
            set => SetValue(WatermarkProperty, value);
        }

        public string Text
        {
            get => GetValue(TextProperty);
            set => SetValue(TextProperty, value);
        }

        public Persona5StyledTextBox()
        {
            InitializeComponent();
            BackgroundPath.UpdateStroke(Colors.White, 2);
            Loaded += GenerateBackground;
        }

        private void GenerateBackground(object? sender, RoutedEventArgs e) =>
            BackgroundPath.UpdateShape((int)Bounds.Width, (int)Bounds.Height, 5, 0, 2);
    }
}
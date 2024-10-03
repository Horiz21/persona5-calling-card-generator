using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using System;

namespace P5CCG
{
    public partial class Persona5StyledButton : UserControl
    {
        public static readonly StyledProperty<Bitmap> DefaultImageProperty =
            AvaloniaProperty.Register<Persona5StyledButton, Bitmap>(nameof(DefaultImage));

        public static readonly StyledProperty<Bitmap> HoverImageProperty =
            AvaloniaProperty.Register<Persona5StyledButton, Bitmap>(nameof(HoverImage));

        public static readonly StyledProperty<Bitmap> PressedImageProperty =
            AvaloniaProperty.Register<Persona5StyledButton, Bitmap>(nameof(PressedImage));

        public static readonly StyledProperty<string> ControlTextContentProperty =
            AvaloniaProperty.Register<Persona5StyledButton, string>(nameof(ControlTextContent));

        public static readonly StyledProperty<bool> IsTextModeProperty =
            AvaloniaProperty.Register<Persona5StyledButton, bool>(nameof(IsTextMode));

        public Bitmap DefaultImage
        {
            get => GetValue(DefaultImageProperty);
            set => SetValue(DefaultImageProperty, value);
        }

        public Bitmap HoverImage
        {
            get => GetValue(HoverImageProperty);
            set => SetValue(HoverImageProperty, value);
        }

        public Bitmap PressedImage
        {
            get => GetValue(PressedImageProperty);
            set => SetValue(PressedImageProperty, value);
        }

        public string ControlTextContent
        {
            get => GetValue(ControlTextContentProperty);
            set => SetValue(ControlTextContentProperty, value);
        }

        public bool IsTextMode
        {
            get => GetValue(IsTextModeProperty);
            set => SetValue(IsTextModeProperty, value);
        }

        private int _boundsHeight = -1, _boundsWidth = -1;

        public Persona5StyledButton()
        {
            InitializeComponent();

            PointerEntered += OnPointerEnter;
            PointerExited += OnPointerLeave;
            PointerPressed += OnPointerPressed;
            PointerReleased += OnPointerReleased;

            Loaded += (_, _) => UpdateAppearance(ButtonState.Default);
        }

        private void UpdateAppearance(ButtonState state)
        {
            if (IsTextMode)
            {
                if (_boundsWidth < 0)
                {
                    _boundsHeight = (int)Bounds.Height;
                    _boundsWidth = (int)Bounds.Width;
                }

                switch (state)
                {
                    case ButtonState.Default:
                        UpdateColor(Colors.Transparent, Colors.White);
                        break;
                    case ButtonState.Hover:
                        UpdateColor(Colors.White, Colors.Black);
                        break;
                    case ButtonState.Pressed:
                        UpdateColor(Colors.White, Colors.Red);
                        break;
                }
            }
            else
            {
                switch (state)
                {
                    case ButtonState.Default:
                        ControlImage.Source = DefaultImage;
                        break;
                    case ButtonState.Hover:
                        ControlImage.Source = HoverImage;
                        break;
                    case ButtonState.Pressed:
                        ControlImage.Source = PressedImage;
                        break;
                }
            }
        }

        private void UpdateColor(Color background, Color foreground)
        {
            BackgroundPath.UpdateShape(_boundsWidth, _boundsHeight, 5, 0, [2.0, 3.5]);
            BackgroundPath.UpdateColor(background);
            ControlText.Foreground = new SolidColorBrush(foreground);
        }

        private void OnPointerEnter(object sender, PointerEventArgs e) => UpdateAppearance(ButtonState.Hover);
        private void OnPointerLeave(object sender, PointerEventArgs e) => UpdateAppearance(ButtonState.Default);

        private void OnPointerPressed(object sender, PointerPressedEventArgs e) =>
            UpdateAppearance(ButtonState.Pressed);

        private void OnPointerReleased(object sender, PointerReleasedEventArgs e)
        {
            UpdateAppearance(ButtonState.Default);
            RaiseClickEvent();
        }

        public event EventHandler? Click;

        private void RaiseClickEvent() => Click?.Invoke(this, EventArgs.Empty);

        private enum ButtonState
        {
            Default,
            Hover,
            Pressed
        }
    }
}
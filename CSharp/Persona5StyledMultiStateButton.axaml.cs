using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Media.Imaging;
using System;
using System.Collections.Generic;
using Avalonia.Media;

namespace P5CCG {
	public partial class Persona5StyledMultiStateButton : UserControl {
        private static readonly StyledProperty<IList<Bitmap>> ControlImageSourcesProperty =
            AvaloniaProperty.Register<Persona5StyledMultiStateButton, IList<Bitmap>>(nameof(ControlImageSources));

        private static readonly StyledProperty<IList<string>> ControlTextContentsProperty =
            AvaloniaProperty.Register<Persona5StyledMultiStateButton, IList<string>>(nameof(ControlTextContents));

        private static readonly StyledProperty<bool> IsTextModeProperty =
            AvaloniaProperty.Register<Persona5StyledMultiStateButton, bool>(nameof(IsTextMode));

        public IList<Bitmap> ControlImageSources
        {
            get => GetValue(ControlImageSourcesProperty);
            init => SetValue(ControlImageSourcesProperty, value);
        }

        public IList<string> ControlTextContents
        {
            get => GetValue(ControlTextContentsProperty);
            init => SetValue(ControlTextContentsProperty, value);
        }

        public bool IsTextMode
        {
            get => GetValue(IsTextModeProperty);
            init => SetValue(IsTextModeProperty, value);
        }

        private int _currentState;

        public Persona5StyledMultiStateButton()
        {
            InitializeComponent();
            BackgroundPath.UpdateColor(Colors.Black);
            Loaded += (_, _) =>
            {
                BackgroundPath.UpdateStroke(Colors.White, 2);
                BackgroundPath.UpdateShape((int)Bounds.Width, (int)Bounds.Height, 5, 0, [2.0, 3.5]);
                UpdateContent();
            };
            
            ControlImageSources = new List<Bitmap>();
            ControlTextContents = new List<string>();
            PointerReleased += OnPointerReleased;
        }

        public int GetCurrentState() => _currentState;

        private void OnPointerReleased(object sender, PointerReleasedEventArgs e)
        {
            var optionCount = Math.Max(ControlImageSources.Count, ControlTextContents.Count);
            if (optionCount <= 0) return;
            _currentState = (_currentState + 1) % optionCount;
            UpdateContent();
            RaiseClickEvent();
        }

        private void UpdateContent()
        {
            switch (IsTextMode)
            {
                case true when ControlTextContents.Count > _currentState:
                    BackgroundPath.UpdateShape((int)Bounds.Width,(int)Bounds.Height,5,0,[2.0, 3.5]);
                    ControlText.Content = ControlTextContents[_currentState];
                    ControlImage.IsVisible = false;
                    ControlText.IsVisible = true;
                    break;
                case false when ControlImageSources.Count > _currentState:
                    ControlImage.Source = ControlImageSources[_currentState];
                    ControlImage.IsVisible = true;
                    ControlText.IsVisible = false;
                    break;
            }
        }

        public event EventHandler? Click;

        private void RaiseClickEvent() => Click?.Invoke(this, EventArgs.Empty);
    }
}

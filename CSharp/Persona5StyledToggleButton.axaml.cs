using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Media.Imaging;
using System;
using System.Diagnostics;
using Avalonia.Markup.Xaml;
using Avalonia.Media;

namespace P5CCG {
	public partial class Persona5StyledToggleButton : UserControl {
		public static readonly StyledProperty<Bitmap> ControlImageSource01Property =
			AvaloniaProperty.Register<Persona5StyledToggleButton, Bitmap>(nameof(ControlImageSource01));

		public static readonly StyledProperty<Bitmap> ControlImageSource02Property =
			AvaloniaProperty.Register<Persona5StyledToggleButton, Bitmap>(nameof(ControlImageSource02));

		public static readonly StyledProperty<Bitmap> ControlImageSource03Property =
			AvaloniaProperty.Register<Persona5StyledToggleButton, Bitmap>(nameof(ControlImageSource03));

		public Bitmap ControlImageSource01 {
			get => GetValue(ControlImageSource01Property);
			set => SetValue(ControlImageSource01Property, value);
		}

		public Bitmap ControlImageSource02 {
			get => GetValue(ControlImageSource02Property);
			set => SetValue(ControlImageSource02Property, value);
		}

		public Bitmap ControlImageSource03 {
			get => GetValue(ControlImageSource03Property);
			set => SetValue(ControlImageSource03Property, value);
		}

		public static readonly StyledProperty<string> ControlTextContent01Property = AvaloniaProperty.Register<Persona5StyledRadioButton, string>(nameof(ControlTextContent01));

		public static readonly StyledProperty<string> ControlTextContent02Property = AvaloniaProperty.Register<Persona5StyledRadioButton, string>(nameof(ControlTextContent02));

		public static readonly StyledProperty<string> ControlTextContent03Property = AvaloniaProperty.Register<Persona5StyledRadioButton, string>(nameof(ControlTextContent03));

		public string ControlTextContent01 {
			get => GetValue(ControlTextContent01Property);
			set => SetValue(ControlTextContent01Property, value);
		}

		public string ControlTextContent02 {
			get => GetValue(ControlTextContent02Property);
			set => SetValue(ControlTextContent02Property, value);
		}

		public string ControlTextContent03 {
			get => GetValue(ControlTextContent03Property);
			set => SetValue(ControlTextContent03Property, value);
		}

		public static readonly StyledProperty<bool> IsTextModeProperty =
			AvaloniaProperty.Register<Persona5StyleButton, bool>(nameof(IsTextMode));

		public bool IsTextMode
		{
			get => GetValue(IsTextModeProperty);
			set => SetValue(IsTextModeProperty, value);
		}

		
		public int currentState = 1;

		public Persona5StyledToggleButton() {
			InitializeComponent();
			BackgroundPath.UpdateColor(Colors.Black);
			Loaded += (sender, args) =>
			{
				PointerReleased += OnPointerReleased;
				BackgroundPath.UpdateStroke(Colors.White, 2);
				BackgroundPath.UpdateShape((int)Bounds.Width, (int)Bounds.Height, 5, 0, [2.0, 3.5]);
			};
		}

		private void OnPointerReleased(object sender, PointerReleasedEventArgs e) {
			currentState = (currentState % 3) + 1;
			Debug.WriteLine(currentState);
			if (IsTextMode)
			{
				BackgroundPath.UpdateShape((int)Bounds.Width,(int)Bounds.Height,5,0,[2.0, 3.5]);
				switch (currentState)
				{
					case 1:
						ControlText.Content = ControlTextContent01;
						break;
					case 2:
						ControlText.Content = ControlTextContent02;
						break;
					case 3:
						ControlText.Content = ControlTextContent03;
						break;
				}
			}
			else
			{
				switch (currentState)
				{
					case 1:
						ControlText.Content = ControlTextContent01;
						break;
					case 2:
						ControlText.Content = ControlTextContent02;
						break;
					case 3:
						ControlText.Content = ControlTextContent03;
						break;
				}
			}
			RaiseClickEvent();
		}

		public event EventHandler Click;

		private void RaiseClickEvent() {
			Click?.Invoke(this, EventArgs.Empty);
		}
	}
}

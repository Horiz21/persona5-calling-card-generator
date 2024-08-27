using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using System;

namespace P5CCG {
	public partial class Persona5StyledRadioButton : UserControl {
		public static readonly StyledProperty<string> GroupNameProperty = AvaloniaProperty.Register<Persona5StyledRadioButton, string>(nameof(GroupName));

		public static readonly StyledProperty<string> ControlTextContentProperty = AvaloniaProperty.Register<Persona5StyledRadioButton, string>(nameof(ControlTextContent));

		public static readonly StyledProperty<bool> RadioButtonIsCheckedProperty = AvaloniaProperty.Register<Persona5StyledRadioButton, bool>(nameof(RadioButtonIsChecked));

		public string GroupName {
			get => GetValue(GroupNameProperty);
			set => SetValue(GroupNameProperty, value);
		}

		public string ControlTextContent {
			get => GetValue(ControlTextContentProperty);
			set => SetValue(ControlTextContentProperty, value);
		}

		public bool RadioButtonIsChecked {
			get => GetValue(RadioButtonIsCheckedProperty);
			set => SetValue(RadioButtonIsCheckedProperty, value);
		}

		public static readonly StyledProperty<Bitmap> ControlImageSourceProperty =
			AvaloniaProperty.Register<Persona5StyleButton, Bitmap>(nameof(ControlImageSource));

		public Bitmap ControlImageSource {
			get => GetValue(ControlImageSourceProperty);
			set => SetValue(ControlImageSourceProperty, value);
		}

		public Persona5StyledRadioButton()
		{
			InitializeComponent();
			MainRadioButton.IsCheckedChanged += GenerateBackground;
			BackgroundPath.UpdateStroke(Colors.White,2);
			Loaded += GenerateBackground;
		}

		private void GenerateBackground(object sender, EventArgs e) {
			if ((bool)MainRadioButton.IsChecked)
			{
				BackgroundPath.UpdateShape((int)Bounds.Width,(int)Bounds.Height,5,0,2);
				BackgroundPath.UpdateColor(Colors.White);
				ControlText.Foreground = Brushes.Black;
			}
			else
			{
				BackgroundPath.UpdateShape((int)Bounds.Width,(int)Bounds.Height,5,0,2);
				BackgroundPath.UpdateColor(Colors.Transparent);
				ControlText.Foreground = Brushes.White;	
			}
		}
	}
}

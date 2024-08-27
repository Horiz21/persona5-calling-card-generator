using Avalonia;
using Avalonia.Controls;
using System;

namespace P5CCG {
	public partial class Persona5StyledDialog : Window {
		public Persona5StyledDialog(WindowBase owner,string title,string text) {
			InitializeComponent();
			Owner = owner;
			Title = title;
			MessageTextBlock.Text = text;
			WindowStartupLocation = WindowStartupLocation.CenterOwner;
			ConfirmButton.Click += (sender, args) => Close();
		}
	}
}

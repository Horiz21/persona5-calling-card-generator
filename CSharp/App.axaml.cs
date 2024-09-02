using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;

namespace P5CCG;

public partial class App : Application
{
    public const string Version = "Beta-240902";
    public const string Link = "https://github.com/Horiz21/persona5-calling-card-generator";
    
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new Generator();
        }

        base.OnFrameworkInitializationCompleted();
    }
}
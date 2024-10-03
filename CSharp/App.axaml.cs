using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Newtonsoft.Json.Linq;

namespace P5CCG;

public class App : Application
{
    public const string Version = "V1.1";
    public const string Link = "https://github.com/Horiz21/persona5-calling-card-generator";
    public static readonly Dictionary<string, string> VersionJsonLink = new Dictionary<string, string>
    {
        { "GitHub", "https://raw.githubusercontent.com/Horiz21/persona5-calling-card-generator/main/version.json" },
        { "Gitee", "https://gitee.com/horiz21/persona5-calling-card-generator/raw/main/version.json" }
    };

    public override void Initialize() => AvaloniaXamlLoader.Load(this);

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            desktop.MainWindow = new Generator();
        base.OnFrameworkInitializationCompleted();
    }
}
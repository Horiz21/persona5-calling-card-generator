using System.Net.Http;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Newtonsoft.Json.Linq;

namespace P5CCG;

public partial class App : Application
{
    public const string Version = "V1.0";
    public const string Link = "https://github.com/Horiz21/persona5-calling-card-generator";

    public const string VersionJsonLinkEn =
        "https://raw.githubusercontent.com/Horiz21/persona5-calling-card-generator/main/version.json";

    public const string VersionJsonLinkCn =
        "https://gitee.com/horiz21/persona5-calling-card-generator/raw/main/version.json";

    public override void Initialize() => AvaloniaXamlLoader.Load(this);

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            desktop.MainWindow = new Generator();
        base.OnFrameworkInitializationCompleted();
    }

    public static async Task<JObject?> FetchJsonAsync(string url)
    {
        using var client = new HttpClient();
        var response = await client.GetAsync(url);
        if (!response.IsSuccessStatusCode) return null;
        var jsonString = await response.Content.ReadAsStringAsync();
        return JObject.Parse(jsonString);
    }
}
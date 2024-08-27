using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Platform;
using Avalonia.Platform.Storage;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace P5CCG;

public partial class Generator : Window
{
    private MemoryStream? _generatedCallingCardStream;

    public Generator()
    {
        InitializeComponent();

        // Basic Button Click Events
        ColorButton.Click += AddRowForColor;
        ContectButton.Click += AddRowForContent;
        GenerateButton.Click += GenerateCallingCardAsync;
        ExportButton.Click += ExportCallingCardAsync;
        FontFolderButton.Click += SelectFontFolder;
        AboutButton.Click += (_, _) =>
            new Persona5StyledDialog(this, "关于",
                "当前版本：20240827（测试版）\n开源地址：https://github.com/Horiz21/persona5-calling-card-generator").Show();

        // Default Values
        AddRowForColor("#FF0000", 260);
        AddRowForColor("#000000", 325);
        AddRowForContent();
    }

    private async void SelectFontFolder(object? sender, EventArgs e)
    {
        var folderPickerOptions = new FolderPickerOpenOptions
        {
            Title = "选择文件夹",
            AllowMultiple = false
        };

        var result = await StorageProvider.OpenFolderPickerAsync(folderPickerOptions);

        if (result is not { Count: > 0 }) return;
        var folderPath = result[0].Path.LocalPath;

        var fontFiles = Directory.EnumerateFiles(folderPath, "*.*", SearchOption.AllDirectories)
            .Where(file => file.EndsWith(".ttf", StringComparison.OrdinalIgnoreCase) ||
                           file.EndsWith(".otf", StringComparison.OrdinalIgnoreCase) ||
                           file.EndsWith(".pfb", StringComparison.OrdinalIgnoreCase) ||
                           file.EndsWith(".pfm", StringComparison.OrdinalIgnoreCase) ||
                           file.EndsWith(".bdf", StringComparison.OrdinalIgnoreCase));

        if (fontFiles.Any())
            FontFolderPath.ControlTextBox.Text = folderPath;
        else
            new Persona5StyledDialog(this, "字体目录错误",
                "所选文件夹中没有找到字体文件。当前版本支持的字体格式为 TrueType (.ttf) 与 OpenType (.otf)。").Show();
    }

    private void AddRowForColor(string hex, int radius)
    {
        var grid = new Grid { ColumnDefinitions = new ColumnDefinitions("75 * 182 * 85 * 40"), Height = 32 };

        var colorPanel = new Persona5StyledTextBox();

        var colorHexTextBox = new Persona5StyledTextBox
        {
            Text = hex,
            Watermark = "#000000"
        };
        var colorWidthTextBox = new Persona5StyledTextBox
        {
            Text = radius.ToString(),
            Watermark = "325"
        };
        var deleteButton = new Persona5StyleButton
        {
            DefaultImage =
                new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_normal.png"))),
            HoverImage = new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_hover.png"))),
            PressedImage =
                new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_pressed.png")))
        };

        colorHexTextBox.ControlTextBox.TextChanged += (_, _) =>
        {
            var newHex = colorHexTextBox.ControlTextBox.Text;
            if (newHex != null && Regex.IsMatch(newHex, @"^#?([A-Fa-f0-9]{6})$"))
            {
                colorPanel.BackgroundPath.UpdateShape(75, 32, 5, 0, 2);
                colorPanel.BackgroundPath.UpdateColor(Color.Parse("#" + newHex[^6..]));
                colorPanel.ControlTextBox.Text = string.Empty;
            }
            else
            {
                colorPanel.BackgroundPath.UpdateColor(Colors.Transparent);
                colorPanel.ControlTextBox.Text = "无效";
            }
        };

        deleteButton.Click += (_, _) =>
        {
            if (ColorStackPanel.Children.Count <= 2)
                new Persona5StyledDialog(this, "无法删除", "至少保留一个颜色-半径组合！").Show();
            else
                ColorStackPanel.Children.Remove(grid);
        };

        colorPanel.ControlTextBox.IsReadOnly = true;
        colorPanel.BackgroundPath.UpdateShape(75, 32, 5, 0, 2);
        colorPanel.BackgroundPath.UpdateColor(Color.Parse(hex));
        grid.Children.Add(colorPanel);
        Grid.SetColumn(colorPanel, 0);
        grid.Children.Add(colorHexTextBox);
        Grid.SetColumn(colorHexTextBox, 2);
        grid.Children.Add(colorWidthTextBox);
        Grid.SetColumn(colorWidthTextBox, 4);
        grid.Children.Add(deleteButton);
        Grid.SetColumn(deleteButton, 6);

        ColorStackPanel.Children.Add(grid);
    }

    private void AddRowForContent(string content = "")
    {
        var grid = new Grid { ColumnDefinitions = new ColumnDefinitions("75 167 * 50 * 50 * 40"), Height = 32 };

        var contentTextBox = new Persona5StyledTextBox();
        if (content.Length > 0) contentTextBox.Text = content;
        contentTextBox.Watermark = "单击此处键入您的文本";
        var fontsizeButton = new Persona5StyledToggleButton
        {
            ControlTextContent01 = "小",
            ControlTextContent02 = "中",
            ControlTextContent03 = "大",
            IsTextMode = true
        };
        var alignmentButton = new Persona5StyledToggleButton
        {
            ControlTextContent01 = "左",
            ControlTextContent02 = "中",
            ControlTextContent03 = "右",
            IsTextMode = true
        };
        var deleteButton = new Persona5StyleButton
        {
            DefaultImage =
                new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_normal.png"))),
            HoverImage = new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_hover.png"))),
            PressedImage =
                new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/button_minus_pressed.png")))
        };

        grid.Children.Add(contentTextBox);
        Grid.SetColumn(contentTextBox, 0);
        Grid.SetColumnSpan(contentTextBox, 2);
        grid.Children.Add(fontsizeButton);
        Grid.SetColumn(fontsizeButton, 3);
        grid.Children.Add(alignmentButton);
        Grid.SetColumn(alignmentButton, 5);
        grid.Children.Add(deleteButton);
        Grid.SetColumn(deleteButton, 7);

        deleteButton.Click += (_, _) =>
        {
            if (ContentStackPanel.Children.Count <= 2)
                new Persona5StyledDialog(this, "无法删除", "至少保留一个文本段落！").Show();
            else ContentStackPanel.Children.Remove(grid);
        };

        ContentStackPanel.Children.Add(grid);
    }

    private void AddRowForColor(object? sender, EventArgs e) => AddRowForColor("#FF0000", 260);
    private void AddRowForContent(object? sender, EventArgs e) => AddRowForContent();

    private async void GenerateCallingCardAsync(object? sender, EventArgs e)
    {
        GeneratedImage.Source = new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/default_light.png")));

        var jsonMap = new JObject
        {
            ["ratio"] = GetSelectedRatio(),
            ["font_path"] = FontFolderPath.Text,
            ["colors"] = GetColorsAndRadii(),
            ["paragraphs"] = GetContents()
        };

        if (!jsonMap["colors"]!.Any())
        {
            new Persona5StyledDialog(this, "无法生成", "含有一个或多个非法的颜色-半径值！").Show();
            return;
        }

        var jsonString = JsonConvert.SerializeObject(jsonMap);
        var escapedArgs = $"--data \"{Escape(jsonString)}\"";

        using var process = new Process();
        process.StartInfo = new ProcessStartInfo
        {
            FileName = "Assets/Binary/cli.exe",
            Arguments = escapedArgs,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        process.Start();
        try
        {
            using var outputStream = new MemoryStream();
            await process.StandardOutput.BaseStream.CopyToAsync(outputStream);
            await process.WaitForExitAsync();

            outputStream.Position = 0;
            GeneratedImage.Source = new Bitmap(outputStream);
            _generatedCallingCardStream = new MemoryStream(outputStream.ToArray());
        }
        catch
        {
            Debug.WriteLine(escapedArgs);
            new Persona5StyledDialog(this, "生成失败",
                    "P5CCG 遇到问题，无法生成，请检查：\n1. 字体目录是否存在且可访问（由于系统限制，P5CCG 可能无法访问系统字体目录，建议自建字体目录）\n2. 字体目录中是否有且仅有 .ttf 和 .otf 格式字体文件")
                .Show();
            new Persona5StyledDialog(this, "生成参数", escapedArgs).Show();
        }
    }

    private async void ExportCallingCardAsync(object? sender, EventArgs e)
    {
        if (_generatedCallingCardStream == null || _generatedCallingCardStream.Length == 0)
        {
            new Persona5StyledDialog(this, "导出失败！", "没有可供导出的图像数据，请先使用生成功能生成并预览，再进行导出。").Show();
            return;
        }

        var topLevel = TopLevel.GetTopLevel(this);
        if (topLevel == null)
        {
            new Persona5StyledDialog(this, "导出失败！", "无法获取当前窗口。").Show();
            return;
        }

        var storageProvider = topLevel.StorageProvider;
        var fileTypes = new FilePickerFileType("PNG 文件")
        {
            Patterns = new[] { "*.png" },
            MimeTypes = new[] { "image/png" }
        };

        var options = new FilePickerSaveOptions
        {
            Title = "保存PNG文件",
            DefaultExtension = ".png",
            SuggestedFileName = "calling_card.png",
            FileTypeChoices = new[] { fileTypes }
        };

        var file = await storageProvider.SaveFilePickerAsync(options);

        if (file != null)
        {
            await SavePngFileAsync(file);
        }
    }

    private async Task SavePngFileAsync(IStorageFile file)
    {
        try
        {
            _generatedCallingCardStream!.Position = 0;
            await using var fileStream = await file.OpenWriteAsync();
            await _generatedCallingCardStream.CopyToAsync(fileStream);
        }
        catch (Exception ex)
        {
            var styledDialog = new Persona5StyledDialog(this, "导出失败！", $"保存图像时遇到错误: {ex.Message}");
            styledDialog.Show();
        }
    }

    private string GetSelectedRatio()
    {
        if ((bool)Ratio01.MainRadioButton.IsChecked!) return "sqrt2:1";
        if ((bool)Ratio02.MainRadioButton.IsChecked!) return "16:9";
        if ((bool)Ratio03.MainRadioButton.IsChecked!) return "4:3";
        return "3:2";
    }

    private JArray GetColorsAndRadii()
    {
        var colorsAndRadii = new JArray();
        foreach (var child in ColorStackPanel.Children.Skip(1))
        {
            if (child is not Grid grid) continue;
            var flagIllegal = (grid.Children[0] as Persona5StyledTextBox)!.ControlTextBox.Text != string.Empty;
            var hex = (grid.Children[1] as Persona5StyledTextBox)!.ControlTextBox.Text;
            var isValidInteger = int.TryParse((grid.Children[2] as Persona5StyledTextBox)!.ControlTextBox.Text,
                out var radius);
            if (flagIllegal || !isValidInteger || radius <= 0) return [];
            colorsAndRadii.Add(new JObject
            {
                { "hex", hex },
                { "radius", radius }
            });
        }

        return colorsAndRadii;
    }

    private JArray GetContents()
    {
        var contents = new JArray();
        foreach (var child in ContentStackPanel.Children.Skip(1))
        {
            if (child is not Grid grid) continue;
            var content = grid.Children[0].FindControl<TextBox>("ControlTextBox")?.Text ?? string.Empty;
            var fontsize = GetToggleButtonState(grid.Children[1] as Persona5StyledToggleButton, "S", "M", "L");
            var alignment = GetToggleButtonState(grid.Children[2] as Persona5StyledToggleButton, "L", "C", "R");

            contents.Add(new JObject
            {
                { "content", content },
                { "fontsize", fontsize },
                { "alignment", alignment },
            });
        }

        return contents;
    }

    private static string GetToggleButtonState(Persona5StyledToggleButton? button, string state1, string state2,
        string state3)
    {
        return button?.currentState switch
        {
            1 => state1,
            2 => state2,
            _ => state3,
        };
    }

    private static string Escape(string str)
    {
        var sb = new StringBuilder();
        foreach (var c in str)
        {
            switch (c)
            {
                case '"':
                    sb.Append("\\\"");
                    break;
                case '\'':
                    sb.Append(@"\'");
                    break;
                case '\n':
                    sb.Append(@"\n");
                    break;
                case '\r':
                    sb.Append(@"\r");
                    break;
                case '\t':
                    sb.Append(@"\t");
                    break;
                default:
                    sb.Append(c);
                    break;
            }
        }

        return sb.ToString();
    }
}
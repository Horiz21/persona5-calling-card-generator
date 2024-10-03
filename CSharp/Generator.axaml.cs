using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Platform;
using Avalonia.Platform.Storage;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.NetworkInformation;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using static Avalonia.Controls.WindowState;

namespace P5CCG;

public partial class Generator : Window
{
    private MemoryStream? _generatedCardFaceStream;
    private MemoryStream? _generatedCardBackStream;

    public Generator()
    {
        InitializeComponent();

        // Advanced Grid
        // Multi-State Button for Image Ratio
        var ratioButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "√2:1", "16:9", "4:3", "3:2", "自动" },
            IsTextMode = true,
        };
        ToolTip.SetTip(ratioButton,
            new ToolTip
            {
                Content = """
                          √2:1：常见纸张的比例，适用于包括 A4、A5、B5 在内的标准尺寸的纸张。
                          16:9：标准宽屏显示器的比例，也是如今手机、数码相机摄影常用的比例之一。
                          4:3：过去显示器的常见比例，也是如今手机、数码相机摄影常用的比例之一。
                          3:2：35 毫米胶片用于静物拍摄的比例，也是常见的照片的印刷比例，适用于 5 吋、6 吋等规格的照片印制。
                          自动：以 3840 像素作为宽度，高度根据内容自适应。
                          """
            });
        AdvancedGrid.Children.Add(ratioButton);
        Grid.SetColumn(ratioButton, 0);

        // Multi-State Button for Custom Color and Radii
        var customColorAndRadiiButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "默认配色", "自定义配色" },
            IsTextMode = true,
        };
        UpdateColorAndRadiiGridVisibility(false);
        ToolTip.SetTip(customColorAndRadiiButton,
            new ToolTip
            {
                Content = """
                          默认配色：P5CCG 将使用 Persona 5 原版的配色风格生成预告信背景。
                          自定义配色：可自由设定同心圆背景各个圆环的半径与色彩。
                          """
            });
        customColorAndRadiiButton.Click += (_, _) =>
            UpdateColorAndRadiiGridVisibility(customColorAndRadiiButton.GetCurrentState() == 1);
        AdvancedGrid.Children.Add(customColorAndRadiiButton);
        Grid.SetColumn(customColorAndRadiiButton, 1);

        // Multi-State Button for Enabling or Disabling Decorative Ink Dots
        var inkDotsButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "生成墨渍", "关闭墨渍" },
            IsTextMode = true
        };
        AdvancedGrid.Children.Add(inkDotsButton);
        ToolTip.SetTip(inkDotsButton,
            new ToolTip
            {
                Content = """
                          生成墨渍：P5CCG 将使用 Persona 5 原版的墨渍效果点缀预告信。
                          关闭墨渍：P5CCG 将生成干净清爽的预告信。
                          """
            });
        Grid.SetColumn(inkDotsButton, 2);

        // Multi-State Button for Enabling or Disabling Card Back Generation
        var cardSidesButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "生成单面", "生成双面" },
            IsTextMode = true
        };
        AdvancedGrid.Children.Add(cardSidesButton);
        ToolTip.SetTip(cardSidesButton,
            new ToolTip
            {
                Content = """
                          生成单面：P5CCG 将仅生成 Persona 5 预告信的正面。
                          生成双面：P5CCG 将同时生成 Persona 5 预告信的正面与绘有心之怪盗团徽标的背面。生成的背面不会展示，仅在导出时一并保存。
                          """
            });
        Grid.SetColumn(cardSidesButton, 3);

        // Click Events for Other Buttons
        AddColorAndRadiiButton.Click += AddColorAndRadii;
        AddColorAndRadii("#FF0000", 260);
        AddColorAndRadii("#000000", 320);

        AddContentButton.Click += AddRowForAddContent;
        AddContent();

        GenerateButton.Click += GenerateCallingCardAsync;
        ExportButton.Click += ExportCallingCardAsync;

        FontDirectoryButton.Click += SelectFontDirectory;

        HelpButton.Click += ShowHelpDialog;

        MinimizeWindowButton.Click += (_, _) => WindowState = Minimized;
        CloseWindowButton.Click += (_, _) => Close();
    }

    /// <summary>
    /// Updated visibility and usability of ColorAndRadii area
    /// </summary>
    /// <param name="isVisible">Determines the visibility and usability of the title and Scroll Viewer of the second input area (ColorAndRadii) on the interface.</param>
    private void UpdateColorAndRadiiGridVisibility(bool isVisible)
    {
        if (isVisible)
        {
            ColorAndRadiiGrid.IsVisible = true;
            ColorAndRadiiScrollViewer.IsVisible = true;
            ContentScrollViewer.Height = 175;
        }
        else
        {
            ColorAndRadiiGrid.IsVisible = false;
            ColorAndRadiiScrollViewer.IsVisible = false;
            ContentScrollViewer.Height = 320;
        }
    }

    /// <summary>
    /// Show the help dialog which contains version information and a "Check Update" Button.
    /// </summary>
    private void ShowHelpDialog(object? sender, EventArgs e)
    {
        var dialog = new Persona5StyledDialog(this, $"""
                                                     当前版本: {App.Version}
                                                     开源地址: {App.Link}
                                                     """);
        dialog.ViceButton.ControlTextContent = "检查更新";
        dialog.ViceButton.Click += async (_, _) =>
        {
            try
            {
                var reply = new Ping().Send("google.com", 1000, "Horiz21"u8.ToArray());
                var source = reply.Status == IPStatus.Success ? "GitHub" : "Gitee";

                using var client = new HttpClient();
                var response = await client.GetAsync(App.VersionJsonLink[source]);
                if (!response.IsSuccessStatusCode)
                    throw new Exception($"无法从网络加载版本列表：{response.StatusCode} - {response.ReasonPhrase}");
                var jsonString = await response.Content.ReadAsStringAsync();
                var jsonContent = JObject.Parse(jsonString);
                var latestVersion = jsonContent.GetValue("latestVersion")?.ToString();

                if (latestVersion == App.Version)
                {
                    dialog.ViceTextBlock.Text = "当前已是最新版本！";
                    dialog.ViceTextBlock.IsVisible = true;
                    dialog.ViceButton.ControlTextContent = "已是最新";
                    dialog.ViceButton.IsEnabled = false;
                }
                else
                {
                    var latestVersionDetails =
                        jsonContent["versions"]?.FirstOrDefault(v => v["version"]?.ToString() == latestVersion);
                    if (latestVersionDetails == null || dialog.ViceButton.ControlTextContent == "下载更新") return;

                    var updateNotes = latestVersionDetails["updateNotes" + source]?.ToString();
                    dialog.ViceTextBlock.Text = updateNotes;
                    dialog.ViceTextBlock.IsVisible = true;
                    dialog.ViceButton.ControlTextContent = "下载更新";
                    dialog.ViceButton.Click += (_, _) =>
                    {
                        var downloadLink = latestVersionDetails["downloadLink" + source]?.ToString();
                        Process.Start(new ProcessStartInfo
                        {
                            FileName = downloadLink,
                            UseShellExecute = true
                        });
                    };
                }
            }
            catch (Exception exception)
            {
                dialog.ViceTextBlock.Text = $"""
                                             {exception.Message}
                                             请检查设备网络接入情况。
                                             """;
                dialog.ViceTextBlock.IsVisible = true;
            }
        };
        dialog.ViceButton.IsVisible = true;

        dialog.ShowDialog(this);
    }

    /// <summary>
    /// Open a select folder window (FolderPicker) for the user to choose a customized font directory.
    /// </summary>
    private async void SelectFontDirectory(object? sender, EventArgs e)
    {
        var directoryPickerOptions = new FolderPickerOpenOptions
        {
            Title = "选择字体目录",
            AllowMultiple = false
        };

        var result = await StorageProvider.OpenFolderPickerAsync(directoryPickerOptions);

        if (result is not { Count: > 0 }) return;
        var directoryPath = result[0].Path.LocalPath;

        var fontExtensions = new[] { ".otf", ".ttf", ".ttc" };
        var fontFiles = Directory.EnumerateFiles(directoryPath, "*.*", SearchOption.AllDirectories)
            .Where(file => fontExtensions.Any(ext => file.EndsWith(ext, StringComparison.OrdinalIgnoreCase)));

        if (fontFiles.Any())
            FontDirectoryTextBox.ControlTextBox.Text = directoryPath;
        else
        {
            var dialog = new Persona5StyledDialog(this, """
                                                        字体目录错误！
                                                        所选文件夹中没有找到字体文件。当前版本支持的字体格式为 TrueType (.ttf) 与 OpenType (.otf)。
                                                        """);
            await dialog.ShowDialog(this);
        }
    }

    private void AddColorAndRadii(string hex, int radius)
    {
        var grid = new Grid { ColumnDefinitions = new ColumnDefinitions("80 * 210 * 85 * 40"), Height = 35 };

        var colorPanel = new Persona5StyledTextBox();

        var colorHexTextBox = new Persona5StyledTextBox
        {
            Text = hex,
            Watermark = "#000000"
        };
        var colorWidthTextBox = new Persona5StyledTextBox
        {
            Text = radius.ToString(),
            Watermark = "320"
        };
        var deleteButton = new Persona5StyledButton
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
                colorPanel.BackgroundPath.UpdateShape(80, 35, 5, 0, [2.0, 3.5]);
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
            if (ColorAndRadiiStackPanel.Children.Count <= 2)
            {
                var dialog = new Persona5StyledDialog(this, """
                                                            无法删除！
                                                            至少保留一个颜色-半径组合！
                                                            """);
                dialog.ShowDialog(this);
            }
            else
                ColorAndRadiiStackPanel.Children.Remove(grid);
        };

        colorPanel.ControlTextBox.IsReadOnly = true;
        colorPanel.BackgroundPath.UpdateShape(80, 35, 5, 0, [2.0, 3.5]);
        colorPanel.BackgroundPath.UpdateColor(Color.Parse(hex));
        grid.Children.Add(colorPanel);
        Grid.SetColumn(colorPanel, 0);
        grid.Children.Add(colorHexTextBox);
        Grid.SetColumn(colorHexTextBox, 2);
        grid.Children.Add(colorWidthTextBox);
        Grid.SetColumn(colorWidthTextBox, 4);
        grid.Children.Add(deleteButton);
        Grid.SetColumn(deleteButton, 6);

        ColorAndRadiiStackPanel.Children.Add(grid);
    }

    private void AddContent(string content = "")
    {
        var grid = new Grid { ColumnDefinitions = new ColumnDefinitions("80 195 * 50 * 50 * 40"), Height = 35 };

        var contentTextBox = new Persona5StyledTextBox();
        if (content.Length > 0) contentTextBox.Text = content;
        contentTextBox.Watermark = "单击此处键入文本";
        var fontSizeButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "小", "中", "大" },
            IsTextMode = true
        };
        var alignmentButton = new Persona5StyledMultiStateButton
        {
            ControlTextContents = new List<string> { "左", "中", "右" },
            IsTextMode = true
        };
        var deleteButton = new Persona5StyledButton
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
        grid.Children.Add(fontSizeButton);
        Grid.SetColumn(fontSizeButton, 3);
        grid.Children.Add(alignmentButton);
        Grid.SetColumn(alignmentButton, 5);
        grid.Children.Add(deleteButton);
        Grid.SetColumn(deleteButton, 7);

        deleteButton.Click += (_, _) =>
        {
            if (ContentStackPanel.Children.Count <= 2)
            {
                var dialog = new Persona5StyledDialog(this, """
                                                            无法删除！
                                                            至少保留一个文本段落！
                                                            """);
                dialog.ShowDialog(this);
            }
            else ContentStackPanel.Children.Remove(grid);
        };

        ContentStackPanel.Children.Add(grid);
    }

    private void AddColorAndRadii(object? sender, EventArgs e) => AddColorAndRadii("#FF0000", 260);
    private void AddRowForAddContent(object? sender, EventArgs e) => AddContent();

    private static readonly string[] RatioArray = ["sqrt2:1", "16:9", "4:3", "3:2", "auto"];
    private static readonly string[] DotsArray = ["dots", "no_dots"];
    private static readonly string[] SidesArray = ["face", "face_and_back"];
    private static readonly string[] FontSizeArray = ["S", "M", "L"];
    private static readonly string[] AlignmentArray = ["L", "C", "R"];

    private async void GenerateCallingCardAsync(object? sender, EventArgs e)
    {
        _generatedCardFaceStream?.SetLength(0);
        _generatedCardBackStream?.SetLength(0);
        GeneratedImage.Source = new Bitmap(AssetLoader.Open(new Uri("avares://P5CCG/Assets/Images/default_light.png")));

        var jsonMap = new JObject
        {
            ["ratio"] = GetButtonState(AdvancedGrid.Children[0] as Persona5StyledMultiStateButton, RatioArray),
            ["fontDirectory"] = GetFontDirectory(),
            ["colorsAndRadii"] = GetColorsAndRadii(),
            ["paragraphs"] = GetContents(),
            ["version"] = App.Version,
            ["dots"] = GetButtonState(AdvancedGrid.Children[2] as Persona5StyledMultiStateButton, DotsArray),
            ["sides"] = GetButtonState(AdvancedGrid.Children[3] as Persona5StyledMultiStateButton, SidesArray),
            ["trigger"] = "avalonia"
        };

        if (jsonMap["colorsAndRadii"]?[0]?.ToString() == "illegal")
        {
            var dialog = new Persona5StyledDialog(this, """
                                                        无法生成！
                                                        含有一个或多个非法的颜色-半径值！
                                                        """);
            await dialog.ShowDialog(this);
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
            CreateNoWindow = true,
            WorkingDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)
        };
        try
        {
            process.Start();
            var output = await process.StandardOutput.ReadToEndAsync();
            Debug.WriteLine(output);
            await process.WaitForExitAsync();

            var json = JObject.Parse(output);
            var faceBase64 = json["face"]!.ToString();
            var faceBytes = Convert.FromBase64String(faceBase64);
            _generatedCardFaceStream = new MemoryStream(faceBytes);
            GeneratedImage.Source = new Bitmap(_generatedCardFaceStream);

            if ((AdvancedGrid.Children[3] as Persona5StyledMultiStateButton)!.GetCurrentState() == 0) return;
            var backBase64 = json["back"]!.ToString();
            var backBytes = Convert.FromBase64String(backBase64);
            _generatedCardBackStream = new MemoryStream(backBytes);
        }
        catch
        {
            Debug.WriteLine(escapedArgs);
            var dialog = new Persona5StyledDialog(this, """
                                                        P5CCG 遇到问题，无法生成。
                                                        请检查字体目录是否存在且目录中有 .ttf/.ttc/.otf 字体文件。
                                                        """);
            await dialog.ShowDialog(this);
        }
    }

    private async void ExportCallingCardAsync(object? sender, EventArgs e)
    {
        if (_generatedCardFaceStream == null || _generatedCardFaceStream.Length == 0)
        {
            var dialog = new Persona5StyledDialog(this, """
                                                        没有可供导出的图像数据！
                                                        请先使用“生成”功能生成预览后再进行导出。
                                                        """);
            await dialog.ShowDialog(this);
            return;
        }

        var topLevel = GetTopLevel(this);

        var storageProvider = topLevel?.StorageProvider;
        var fileTypes = new FilePickerFileType("PNG 文件")
        {
            Patterns = new[] { "*.png" },
            MimeTypes = new[] { "image/png" }
        };

        var options = new FilePickerSaveOptions
        {
            Title = "保存预告信正面 PNG 文件",
            DefaultExtension = ".png",
            SuggestedFileName = "Calling Card.png",
            FileTypeChoices = new[] { fileTypes }
        };

        var file = await storageProvider?.SaveFilePickerAsync(options)!;
        if (file != null) await SavePngFileAsync(file, 0);

        if ((AdvancedGrid.Children[3] as Persona5StyledMultiStateButton)!.GetCurrentState() == 0) return;
        var optionsBack = new FilePickerSaveOptions
        {
            Title = "保存预告信背面 PNG 文件",
            DefaultExtension = ".png",
            SuggestedFileName = "Calling Card (Back).png",
            FileTypeChoices = new[] { fileTypes }
        };
        var fileBack = await storageProvider.SaveFilePickerAsync(optionsBack);
        if (fileBack != null) await SavePngFileAsync(fileBack, 1);
    }

    private async Task SavePngFileAsync(IStorageFile file, int side)
    {
        try
        {
            if (side == 0)
            {
                _generatedCardFaceStream!.Position = 0;
                await using var fileStream = await file.OpenWriteAsync();
                await _generatedCardFaceStream.CopyToAsync(fileStream);
            }
            else // side == 1
            {
                _generatedCardBackStream!.Position = 0;
                await using var fileStream = await file.OpenWriteAsync();
                await _generatedCardBackStream.CopyToAsync(fileStream);
            }
        }
        catch (Exception ex)
        {
            var styledDialog = new Persona5StyledDialog(this, $"""
                                                               导出失败！
                                                               保存图像时遇到错误: {ex.Message}。
                                                               """);
            await styledDialog.ShowDialog(this);
        }
    }

    private string GetFontDirectory()
    {
        var fontDirectory = FontDirectoryTextBox.Text;
        return string.IsNullOrEmpty(fontDirectory) ? "default" : fontDirectory;
    }

    private JToken GetColorsAndRadii()
    {
        if ((AdvancedGrid.Children[1] as Persona5StyledMultiStateButton)!.GetCurrentState() == 0)
            return new JArray("default");
        var colorsAndRadii = new JArray();
        foreach (var child in ColorAndRadiiStackPanel.Children.Skip(1))
        {
            if (child is not Grid grid) continue;
            var flagIllegal = (grid.Children[0] as Persona5StyledTextBox)!.ControlTextBox.Text != string.Empty;
            var hex = (grid.Children[1] as Persona5StyledTextBox)!.ControlTextBox.Text;
            var isValidInteger = int.TryParse((grid.Children[2] as Persona5StyledTextBox)!.ControlTextBox.Text,
                out var radius);
            if (flagIllegal || !isValidInteger || radius <= 0) return new JArray("illegal");
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
            var fontSize = GetButtonState(grid.Children[1] as Persona5StyledMultiStateButton, FontSizeArray);
            var alignment = GetButtonState(grid.Children[2] as Persona5StyledMultiStateButton, AlignmentArray);

            contents.Add(new JObject
            {
                { "content", content },
                { "fontSize", fontSize },
                { "alignment", alignment },
            });
        }

        return contents;
    }

    private static string GetButtonState(Persona5StyledMultiStateButton? button, IReadOnlyList<string> states) =>
        states[button!.GetCurrentState()];

    private readonly Dictionary<char, string> _escapeSequences = new()
    {
        { '"', "\\\"" },
        { '\'', "\\'" },
        { '\n', "\\n" },
        { '\r', "\\r" },
        { '\t', "\\t" }
    };

    private string Escape(string str)
    {
        var sb = new StringBuilder();
        foreach (var c in str)
        {
            if (_escapeSequences.TryGetValue(c, out var escaped))
                sb.Append(escaped);
            else
                sb.Append(c);
        }

        return sb.ToString();
    }
}
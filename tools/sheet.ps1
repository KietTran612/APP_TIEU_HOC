param([string]$Dir, [string[]]$Ids, [string]$Out, [int]$Cols = 5, [int]$Thumb = 220)
Add-Type -AssemblyName System.Drawing
$rows = [math]::Ceiling($Ids.Count / $Cols)
$cellH = $Thumb + 26
$bmp = New-Object System.Drawing.Bitmap ($Cols * $Thumb), ($rows * $cellH)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::White)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$font = New-Object System.Drawing.Font 'Arial', 9
for ($i = 0; $i -lt $Ids.Count; $i++) {
    $x = ($i % $Cols) * $Thumb; $y = [math]::Floor($i / $Cols) * $cellH
    $p = Join-Path $Dir ($Ids[$i] + '.png')
    if (Test-Path $p) {
        $img = [System.Drawing.Image]::FromFile($p)
        $g.DrawImage($img, $x + 4, $y + 4, $Thumb - 8, $Thumb - 8)
        $img.Dispose()
    }
    $g.DrawString($Ids[$i], $font, [System.Drawing.Brushes]::Black, $x + 4, $y + $Thumb + 4)
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
"saved $Out"

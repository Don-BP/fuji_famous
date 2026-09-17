$ErrorActionPreference = "Stop"

# All Japanese text (paths, labels, content) lives in the JSON, read as UTF-8.
# This script stays pure ASCII so PowerShell 5.1 cannot mangle it.
$json = "D:\Fuji_Famous\tools\entry_fields.json"
$f = (Get-Content $json -Raw -Encoding UTF8) | ConvertFrom-Json

$w = New-Object -ComObject Word.Application
$w.Visible = $true   # hidden Word hung on open; visible is reliable
$w.DisplayAlerts = 0
$d = $w.Documents.Open($f.src, $false, $false)

function Set-AfterLabel($doc, $label, $text) {
    foreach ($p in $doc.Paragraphs) {
        $t = ($p.Range.Text -replace "[`r`a]", "").Trim()
        if ($t.StartsWith($label)) {
            $r = $p.Range
            $r.MoveEnd(1, -1) | Out-Null   # exclude the paragraph mark
            $r.InsertAfter($text)
            return $true
        }
    }
    Write-Warning "label not found: $label"
    return $false
}

Set-AfterLabel $d $f.labels.rep     $f.rep                     | Out-Null
Set-AfterLabel $d $f.labels.members $f.members                 | Out-Null
Set-AfterLabel $d $f.labels.group   $f.group                   | Out-Null
Set-AfterLabel $d $f.labels.idea    $f.idea                    | Out-Null
Set-AfterLabel $d $f.labels.summary ("`r" + $f.summary)        | Out-Null
Set-AfterLabel $d $f.labels.effect  ("`r" + $f.effect)         | Out-Null

# The effect box grew past the page when the 2027 scenes went in, so the
# whole box (summary and effect) is set a little smaller. Size lives in JSON.
if ($f.boxFontSize) {
    $inBox = $false
    foreach ($p in $d.Paragraphs) {
        $t = ($p.Range.Text -replace "[`r`a]", "").Trim()
        if ($t.StartsWith($f.labels.summary)) { $inBox = $true }
        if ($t.StartsWith($f.labels.stop))    { $inBox = $false }
        if ($inBox) { $p.Range.Font.Size = $f.boxFontSize }
    }
}

$d.SaveAs2($f.dest, 12)   # wdFormatXMLDocument
$d.Close($false)
$w.Quit()

"SAVED " + $f.dest

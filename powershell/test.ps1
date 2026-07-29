$Host.UI.RawUI.ForegroundColor = 'Black'
$Host.UI.RawUI.BackgroundColor = ($bckgrnd = 'White')
$Host.PrivateData.ErrorForegroundColor = 'Red'
$Host.PrivateData.ErrorBackgroundColor = "White"
$Host.PrivateData.WarningForegroundColor = 'Black'
$Host.PrivateData.WarningBackgroundColor = "White"
$Host.PrivateData.DebugForegroundColor = 'Black'
$Host.PrivateData.DebugBackgroundColor = "White"
$Host.PrivateData.VerboseForegroundColor = 'Black'
$Host.PrivateData.VerboseBackgroundColor = "White"
Set-PSReadLineOption -Colors @{ variable = "`e[38;2;0;0;0m" + # fg
                                           "`e[48;2;255;255;255m" } # bg

powershell

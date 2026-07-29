$MethodDefinition = @'
[DllImport("user32.dll", CharSet = CharSet.Unicode)]
public static extern bool SetWindowPos(IntPtr hWnd, int hWndInsertAfter, int X, int Y, int cx, int cy, int wFlags);
'@
$User32 = Add-Type -MemberDefinition $MethodDefinition -Name 'User32' -Namespace 'Win32' -PassThru
$screen = Add-Type -AssemblyName System.Windows.Forms
$width = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$height = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height
#$width = Get-WmiObject -Class Win32_DesktopMonitor | Select-Object -expand ScreenWidth
$intwidth = [int]$width
#$height = Get-WmiObject -Class Win32_DesktopMonitor | Select-Object -expand ScreenHeight
$intheight = [int]$height
$CurrentProcess = Get-Process -id $PID
$User32::SetWindowPos($CurrentProcess.MainWindowHandle, 0x0, $intwidth/2, 0, $intwidth/1.97, $intheight/1.97, 0x0040 -bor 0x0020)
cd "C:\pierre\apps\python apps\echolumena\connection"
echo "positionning done"
cmd /c "color f1"
echo "========Chatting with instrument========"
py pTestEchoLumena_v18.py 3 3
PowerShell

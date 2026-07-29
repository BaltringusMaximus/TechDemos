Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
$MethodDefinition2 = @'
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
public static extern uint GetLastError();
'@
$kernel32 = Add-Type -MemberDefinition $MethodDefinition2 -Name 'kernel32' -Namespace 'Win32' -PassThru
$kernel32::GetLastError()
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
echo $CurrentProcess
echo $PID
#echo "printing window handle then the related error"
$CurrentProcess.MainWindowHandle
$kernel32::GetLastError()
echo "printing error code after setwindowpos"
$User32::SetWindowPos($CurrentProcess.MainWindowHandle, 0x0, 0, 0, $intwidth/1.97, $intheight/1.97, 0x0040 -bor 0x0020)
$kernel32::GetLastError()
echo "positionning done"
#New-PSDrive -Name "I" -PSProvider FileSystem -Root "\\10.14.1.234\e"
#Get-ChildItem I:
echo "========Generating Graphs and Results========"
cd "C:\pierre\apps\python apps\graphgen"
py pGraphResProcessor_v3.py
PowerShell

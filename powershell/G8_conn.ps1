#$desktopSessionId = '2'
$username = 'cosem.fr\supportroche'
$password = '3/J;K5ygA76r$c'
$credentials = New-Object System.Management.Automation.PSCredential -ArgumentList @($username,(ConvertTo-SecureString -String $password -AsPlainText -Force))
$client = 'SRV6-COBAS04'
function startG8Remotely($client) {
     PsExec.exe -i $desktopSession.GetValue(1)[43] -d \\$client -u cosem.fr\supportroche -p '3/J;K5ygA76r$c' CMD /k "taskkill /F /IM python.exe & taskkill /F /IM powershell.exe & cd C:\pierre\apps\ps1 & dir & start ps_conn_G8.ps1"
}
$MethodDefinition2 = @'
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
public static extern uint GetLastError();
'@
$kernelerror = Add-Type -MemberDefinition $MethodDefinition2 -Name 'kernel32' -Namespace 'Win32' -PassThru
Write-Host last error = $kernelerror::GetLastError()
Write-Host Opening RDP Session to register a session
cmdkey /add:'SRV6-COBAS04' /user:'cosem.fr\supportroche' /pass:'3/J;K5ygA76r$c'
mstsc /v:SRV6-COBAS04 /f
Write-Host Opening PSSession to acquire session ID
$i=0
while($i -ne 30)
{
	try
	{
		write-host trying to retrieve the session ID
		$desktopSession = Invoke-Command -ComputerName SRV6-COBAS04 -Credential $credentials -ScriptBlock {query user /server:'SRV6-COBAS04'} -ErrorAction stop
		$i=30
	}
	catch 
	{
		write-host caught the exception $i
		start-sleep -seconds 1
		$i++
	}
}
Write-Host desktopSession = $desktopSession
$ID = $desktopSession.GetValue(1)[43]
Write-Host session ID = $ID
startG8Remotely($client)
Write-Host last error = $kernelerror::GetLastError()
#     $desktopSession = query user /server:$client | Select-String -Pattern Active
#     $ID = ($desktopSession -split '\s+')[3]
powershell
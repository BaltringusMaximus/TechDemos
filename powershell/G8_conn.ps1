#$desktopSessionId = '2'
$username = 'USERNAME'
$password = 'PASSWORD'
$credentials = New-Object System.Management.Automation.PSCredential -ArgumentList @($username,(ConvertTo-SecureString -String $password -AsPlainText -Force))
$client = 'CLIENT'
function startG8Remotely($client) {
     PsExec.exe -i $desktopSession.GetValue(1)[43] -d \\$client -u $username -p $password CMD /k "taskkill /F /IM python.exe & taskkill /F /IM powershell.exe & cd C:\pierre\apps\ps1 & dir & start ps_conn_G8.ps1"
}
$MethodDefinition2 = @'
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
public static extern uint GetLastError();
'@
$kernelerror = Add-Type -MemberDefinition $MethodDefinition2 -Name 'kernel32' -Namespace 'Win32' -PassThru
Write-Host last error = $kernelerror::GetLastError()
Write-Host Opening RDP Session to register a session
cmdkey /add:$client /user:$username /pass:$password
mstsc /v:$client /f
Write-Host Opening PSSession to acquire session ID
$i=0
while($i -ne 30)
{
	try
	{
		write-host trying to retrieve the session ID
		$desktopSession = Invoke-Command -ComputerName $client -Credential $credentials -ScriptBlock {query user /server:$client} -ErrorAction stop
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

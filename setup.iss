;
; /setup.iss
;    Script for the open source Inno Setup Compiler (requires ISSI)
;
; Copyright © 2012 Malte Bublitz. All rights reserved.
; 
; Redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions are met:
; 
;  1. Redistributions of source code must retain the above copyright notice,
;     this list of conditions and the following disclaimer.
;
;  2. Redistributions in binary form must reproduce the above copyright notice,
;     this list of conditions and the following disclaimer in the documentation
;     and/or other materials provided with the distribution.
; 
; THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
; INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
; FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR
; AND/OR CONTRIBUTORS OF WindowsInfo BE LIABLE FOR ANY DIRECT, INDIRECT,
; INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
; LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
; PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
; LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
; OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
; ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
; 

#define MyAppName "Windows Info"
#define MyAppVersion "0.2.1"
#define MyAppPublisher "Malte Bublitz"
#define MyAppExeName "WindowsInfo.exe"
#define MyAppURL "https://malte-bublitz.de/WindowsInfo.html"

[Setup]
AppID={{1DB90294-CFD6-4467-90F2-39022695E26A}
AppName=Windows Info
AppVersion=0.2.1
AppVerName=Windows Info 0.2.1
AppPublisher=Malte Bublitz
AppSupportURL="https://malte-bublitz.de/WindowsInfo.html"
AppCopyright=Copyright © 2012 Malte Bublitz
DefaultDirName="{pf}\Windows Info"
DefaultGroupName="Windows Info"
OutputDir=C:\Users\Malte\Documents\WindowsInfo\dist
OutputBaseFilename=WindowsInfo-0.2-setup
Compression=lzma2/Max
SolidCompression=true
ArchitecturesAllowed=x64 x86
UninstallDisplayIcon={app}\WindowsInfo.exe
ArchitecturesInstallIn64BitMode=x64
MinVersion=0,5.1.2600
VersionInfoVersion=0.2.1
VersionInfoTextVersion=0.2.1
VersionInfoCompany=Malte Bublitz
VersionInfoDescription=Windows Info Setup Assistant
VersionInfoCopyright=Copyright © 2012 Malte Bublitz
VersionInfoProductName=WindowsInfo
VersionInfoProductVersion=0.2.1
UninstallDisplayName=Malte's Windows Info
PrivilegesRequired=poweruser
SignTool=MalteBublitzOSS /d $qWindows Info$q $f
AppContact=mailto:me@malte-bublitz.de
SetupIconFile=C:\Users\Malte\Documents\WindowsInfo\ressources\Setup.ico
ShowLanguageDialog=auto

[Languages]
Name: english; MessagesFile: compiler:Default.isl 
Name: german; MessagesFile: compiler:Languages\German.isl 

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "desktopicon\common"; Description: "{cm:ForAllUsers}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: exclusive unchecked
Name: "desktopicon\user"; Description: "{cm:ForTheCurrentUserOnly}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: exclusive unchecked

[Files]

Source: C:\Users\Malte\Documents\WindowsInfo\build\exe.win-amd64-2.7\*; DestDir: {app}; Flags: ignoreversion; Check: Is64BitInstallMode 

Source: C:\Users\Malte\Documents\WindowsInfo\build\exe.win32-2.7\*; DestDir: {app}; Flags: ignoreversion; Check: not Is64BitInstallMode 

Source: C:\Users\Malte\Documents\WindowsInfo\ressources\Setup.ico; DestDir: {app} 
Source: C:\Users\Malte\Documents\WindowsInfo\ressources\help.en.html; DestDir: {app}; DestName: Help.html; Languages: english 
Source: C:\Users\Malte\Documents\WindowsInfo\ressources\help.de.html; DestDir: {app}; DestName: Help.html; Languages: german 

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
;Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent
;Filename: "{app}\ReadMe.html"; Description: "{cm:Readme}"; Flags: postinstall shellexec skipifsilent SkipIfDoesntExist Unchecked; 

[Registry]
Root: HKLM; SubKey: "Software\Malte Bublitz\WindowsInfo"; ValueType: none; Flags: UninsDeleteKeyIfEmpty UninsDeleteValue;
Root: HKLM; SubKey: "Software\Malte Bublitz\WindowsInfo"; ValueType: string; ValueName: Path; ValueData: {app}; Flags: UninsDeleteValue;
Root: HKLM; SubKey: "Software\Malte Bublitz\WindowsInfo"; ValueType: string; ValueName: InstalledLanguage; ValueData: {language}; Flags: UninsDeleteValue;

[CustomMessages]
english.Readme=View README
german.Readme=LIESMICH anzeigen
english.ForAllUsers=For all users
german.ForAllUsers=Für alle Benutzer
english.ForTheCurrentUserOnly=For the current user only
german.ForTheCurrentUserOnly=Nur für den aktuellen Benutzer
english.ExpressInstall=Express installation
german.ExpressInstall=Express-Installation

[Messages]
BeveledLabel=Copyright © 2012 Malte Bublitz

[Code]
var
  cb1 : TCheckBox;

function CreateCheckbox(const X, Y, Width: integer; Caption: string;
  Parent: TWinControl; ClickEvent: TNotifyEvent): TCheckBox;
begin
  Result := TCheckBox.Create(WizardForm);
  if Result <> nil then
  begin
    Result.Left    := X;
    Result.Top     := Y;
    Result.Width   := Width;
    Result.Caption := Caption;
    Result.Checked := true;
    Result.Parent  := Parent;
    Result.OnClick := ClickEvent;
  end;
end;
function ShouldSkipPage(PageId: integer): boolean;
begin
  case PageId of
    // Auswahl des Zielverzeichnisses
    wpSelectDir,
    // Auswahl der Programmgruppe im Startmenü
    wpSelectProgramGroup,
    // Auswahl der zu installierenden Komponenten
    wpSelectComponents,
    // Auswahl der zusätzlichen Aufgaben
    wpSelectTasks,
    // Anzeige der Zusammenfassung vor der Installation
    wpReady:
      Result := cb1.Checked;
    else
      Result := false;
  end;
end;
procedure CurPageChanged(CurrentPageId: Integer);
begin
  if CurrentPageId = wpLicense then
  begin
    if cb1.Checked then
      WizardForm.NextButton.Caption := SetupMessage(msgButtonInstall)
    else
      WizardForm.NextButton.Caption := SetupMessage(msgButtonNext);
  end;
end;
procedure InitializeWizard;
begin
  cb1 := CreateCheckBox(WizardForm.WelcomeLabel2.Left, WizardForm.WelcomeLabel2.Top + WizardForm.WelcomeLabel2.Height - 30, 120, CustomMessage('ExpressInstall'), WizardForm.WelcomePage, nil);
end;


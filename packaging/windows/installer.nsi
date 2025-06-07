
; OSLolo NSIS Installer Script

!define PRODUCT_NAME "OSLolo"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Universidad Team"
!define PRODUCT_WEB_SITE "https://github.com/universidad-team/oslolo"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_ICON "oslolo.ico"
!define APP_EXE "oslolo.exe"

; --- Includes ---
!include "MUI2.nsh"

; --- General ---
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "oslolo-${PRODUCT_VERSION}-setup.exe"
InstallDir "$PROGRAMFILES64\${PRODUCT_NAME}"
InstallDirRegKey HKCU "${PRODUCT_UNINST_KEY}" "InstallLocation"
RequestExecutionLevel admin
SetCompressor lzma

; --- Interface Settings ---
!define MUI_ABORTWARNING
!define MUI_ICON "${PRODUCT_ICON}"
!define MUI_UNICON "${PRODUCT_ICON}"

; --- Pages ---
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; --- Language ---
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Spanish"


; --- Installer Section ---
Section "Install"
  SetOutPath $INSTDIR
  
  ; Files to install
  File /r "dist\oslolo\" ; Assumes pyinstaller output is in dist/oslolo
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  ; Write registry keys
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${APP_EXE}"

  ; Add to Start Menu
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${APP_EXE}"

  ; Add to Path (optional)
  EnVar::SetHKLM "PATH" "$INSTDIR"

SectionEnd

; --- Uninstaller Section ---
Section "Uninstall"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR"
  
  ; Remove Start Menu entry
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
  
  ; Remove registry keys
  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  
  ; Remove from Path (optional)
  EnVar::DeleteHKLM "PATH" "$INSTDIR"

SectionEnd

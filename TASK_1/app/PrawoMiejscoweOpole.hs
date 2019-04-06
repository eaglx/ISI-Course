
{-# LANGUAGE Arrows, NoMonomorphismRestriction, FlexibleContexts #-}
import ShadowLibrary.Core

import Text.XML.HXT.Core
import Text.XML.HXT.XPath
--import Text.XML.HXT.Curl
import Data.List
import Data.List.Utils (replace)

import Text.Regex.Posix
import Text.Printf

myver_baseMonthNameToNumber :: String -> String
myver_baseMonthNameToNumber "styczeń"     =  "01"
myver_baseMonthNameToNumber "styczen"     =  "01"
myver_baseMonthNameToNumber "stycznia"     =  "01"
myver_baseMonthNameToNumber "luty"        =  "02"
myver_baseMonthNameToNumber "lutego"        =  "02"
myver_baseMonthNameToNumber "marzec"      =  "03"
myver_baseMonthNameToNumber "marca"      =  "03"
myver_baseMonthNameToNumber "kwiecień"    =  "04"
myver_baseMonthNameToNumber "kwiecien"    =  "04"
myver_baseMonthNameToNumber "kwietnia"    =  "04"
myver_baseMonthNameToNumber "maj"         =  "05"
myver_baseMonthNameToNumber "maja"         =  "05"
myver_baseMonthNameToNumber "czerwiec"    =  "06"
myver_baseMonthNameToNumber "czeerwiec"    =  "06"
myver_baseMonthNameToNumber "czerwca"    =  "06"
myver_baseMonthNameToNumber "lipiec"      =  "07"
myver_baseMonthNameToNumber "lipca"      =  "07"
myver_baseMonthNameToNumber "sierpień"    =  "08"
myver_baseMonthNameToNumber "sierpien"    =  "08"
myver_baseMonthNameToNumber "sierpnia"    =  "08"
myver_baseMonthNameToNumber "wrzesień"    =  "09"
myver_baseMonthNameToNumber "wrzesien"    =  "09"
myver_baseMonthNameToNumber "września"    =  "09"
myver_baseMonthNameToNumber "wrzesnia"    =  "09"
myver_baseMonthNameToNumber "październik" =  "10"
myver_baseMonthNameToNumber "pażdziernik" =  "10"
myver_baseMonthNameToNumber "pazdziernik" =  "10"
myver_baseMonthNameToNumber "października" =  "10"
myver_baseMonthNameToNumber "pazdziernika" =  "10"
myver_baseMonthNameToNumber "listopad"    =  "11"
myver_baseMonthNameToNumber "listopada"    =  "11"
myver_baseMonthNameToNumber "grudzień"    =  "12"
myver_baseMonthNameToNumber "grudzien"    =  "12"
myver_baseMonthNameToNumber "grudnia"    =  "12"
myver_baseMonthNameToNumber "jesien"    =  "10"
myver_baseMonthNameToNumber _             = ""


extractRecords = extractLinksWithText "//div[@class='rocznik']/div/p/a"
                >>> second (arr $ replace "                                 " "")
                >>> first (extractLinksWithText "//div[@class='uchwala-area']/div/p/a")
                >>> first(second (arr $ replace "                                 " ""))
                >>> first (first (extractLinksWithText "//ul[@class='attachements-list']/li/a[not(contains(@href, 'mailto')) and contains(@href,'.pdf')]"))
                >>> first(first(second (arr $ replace "                                 " "")))

toShadowItem :: (((String, String), String), String) -> ShadowItem
toShadowItem (((url, blaTitle), articleTitle), yearlyTitle) =
  (defaultShadowItem url title) {
    originalDate = Just date,
    itype = "periodical",
    format = Just "pdf",
    finalUrl = url
    }
  where title = "Prawo Miejscoe Opole " ++ " blaTitle: " ++ blaTitle  ++ " "  ++ yearlyTitle ++ " " ++ (replace "\r\n" "" (replace "\r\n          " "" articleTitle))
        date = getDate articleTitle

getDate url =
  case url =~~ ".*z dnia ([0-9]{1,2} [A-Za-z]* [0-9]{4}).*" :: Maybe [[String]] of
    Just [[_, year]] -> workWithYear year
    otherwise -> ("unexpected date")

workWithDay x =
  case length x of
    1 -> "0" ++ x
    _ -> x

workWithYear text = do
  let (_, _, _, [day, month, year]) = text =~ "([0-9]+) ([A-Za-z]*) ([0-9]*)" :: (String,String,String,[String])
  year ++ "-" ++ myver_baseMonthNameToNumber month ++ "-" ++ workWithDay day

main = do
    let start = "https://prawomiejscowe.um.opole.pl/institution/18386/yearbooks"
    let shadowLibrary = ShadowLibrary {logoUrl=Nothing,
                                       lname="PrawoMiejscoweOpole",
                                       abbrev="PraMiejOpol",
                                       lLevel=0,
                                       webpage=start}
    extractItemsStartingFromUrl shadowLibrary start (extractRecords >>> arr toShadowItem)

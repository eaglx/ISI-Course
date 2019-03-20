
{-# LANGUAGE Arrows, NoMonomorphismRestriction, FlexibleContexts #-}
import ShadowLibrary.Core

import Text.XML.HXT.Core
import Text.XML.HXT.XPath
--import Text.XML.HXT.Curl
import Data.List
import Data.List.Utils (replace)

import Text.Regex.Posix
import Text.Printf

--extractRecords = extractLinksWithText "//a[@class='roczniki']"
--                 >>> second (arr $ replace "\r\n              " "")
--                 >>> first (arr ((++"tr") . init))
--                 >>> first (extractLinksWithText "//li/a[contains(@href,'.pdf')]")

--extractInnerHtml xpathCondition

extractRecords = extractLinksWithText "//div[@class='rocznik']/div/p/a[@href='/institution/18386/yearbook/2019/January']"
                >>> second (arr $ replace "                                 " "")
                >>> first (extractLinksWithText "//div[@class='uchwala-area']/div/p/a")
                >>> first(second (arr $ replace "                                 " ""))
                -- >>> second (extractInnerHtml)
                >>> first (first (extractLinksWithText "//ul[@class='attachements-list']/li/a[not(contains(@href, 'mailto')) and contains(@href,'.pdf')]"))
                >>> first(first(second (arr $ replace "                                 " "")))

--toShadowItem :: ((String, String), String) -> ShadowItem
--toShadowItem ((url, articleTitle), yearlyTitle) =
--  (defaultShadowItem url title) {
--    originalDate = Just date,
--    itype = "periodical",
--    format = Just "pdf",
--    finalUrl = url
--    }
--  where title = "Almanach Muszyny " ++ yearlyTitle ++ " " ++ (replace "\r\n" "" (replace "\r\n          " "" articleTitle))
--        date = getDate url

-- New
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
  case url =~~ ".*z dnia ([0-9]{2} [A-Za-z]* [0-9]{4}).*" :: Maybe [[String]] of
    Just [[_, year]] -> year
    otherwise -> ("unexpected date")


main = do
    let start = "https://prawomiejscowe.um.opole.pl/institution/18386/yearbooks"
    let shadowLibrary = ShadowLibrary {logoUrl=Nothing,
                                       lname="PrawoMiejscoweOpole",
                                       abbrev="PraMiejOpol",
                                       lLevel=0,
                                       webpage=start}
    extractItemsStartingFromUrl shadowLibrary start (extractRecords >>> arr toShadowItem)

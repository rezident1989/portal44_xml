# Формирование XML пакетов

<details><summary>Подтверждение</summary><br>

**Предусловие:**<br>
Шаблон: **confirmation.xml**<br>
Результат взаимодействия с ЕИС: "Ожидание обработки"<br>

    <id> - 36 символов
    <loadId> - 8 цифр
    <refId> - текст <id> исходящего файла

**Ожидаемый результат:**<br>
Результат взаимодействия с ЕИС: "Успешно"
___
</details>

<details><summary>Добавление позиции (особой позиции) в опубликованный в ЕИС план-график</summary><br>

**Предусловие:**<br>
Шаблон: **tenderPlan2020.xml**<br>
TODO

    <id> - 8 цифр
    <externalId> - текст <externalId> исходящего файла   
    <planNumber> - текст <planNumber> исходящего файла
    <versionNumber> - текст <versionNumber> исходящего файла
    <confirmDate> - текст <createDateTime> исходящего файла
    
    <positions> # если обычная позиция плана-графика
        <commonInfo><positionNumber> - 24 цифр
        <commonInfo><extNumber> - текст <extNumber> исходящего файла
        <commonInfo><IKZ> - текст <IKZ> исходящего файла, !!! если НЕТ: 36 цифр !!!
        <commonInfo><publishYear> - текст <publishYear> исходящего файла
        <commonInfo><IKU> - текст <IKU> исходящего файла,  !!! если НЕТ: 20 цифр !!!
        <commonInfo><purchaseNumber> - текст <purchaseNumber> исходящего файла
    </position>

    <specialPurchasePositions> # если особая позиция плана-графика
        <positionNumber> - 24 цифр
        <extNumber> - текст <extNumber> исходящего файла
        <IKZ> - текст <IKZ> исходящего файла,  !!! если НЕТ: 36 цифр !!!
        <publishYear> - текст <publishYear> исходящего файла
        <IKU> - текст <IKU> исходящего файла,  !!! если НЕТ: 20 цифр !!!
        <purchaseNumber> - текст <purchaseNumber> исходящего файла
    </specialPurchasePosition>

**Ожидаемый результат:**<br>
Статус плана-графика: "Опубликован в ЕИС"<br>
Статус позиции (особой позиции) плана-графика: "Включена в опубликованный в ЕИС план-график"
___
</details>

<details><summary>Извещение. Электронный аукцион</summary>

## 1. Подача ценовых предложений
**Предусловие:**<br>
Шаблон: **epNotificationEF.xml**<br>
TODO

    <id> - 8 цифр
    <externalId> - текст <externalId> исходящего файла
    <ns5:commonInfo>
        <purchaseNumber> - 19 цифр
        <docNumber> - 19 цифр
    </ns5:commonInfo>
    <plannedPublishDate> - текст <plannedPublishDate> исходящего файла
    <publishDTInEIS> - текущая дата в исходном формате
    <purchaseObjectInfo> - текст <purchaseObjectInfo> исходящего файла  
    <docDate> - все теги в шаблоне меняем на текущую дату в исходном формате
    <endDT> - текст <endDT> исходящего файла 
    <summarizingDate> - текст <summarizingDate> исходящего файла 
    <stageInfo>
        <sid> - 7 цифр
        <externalSid> - текст <externalSid> исходящего файла
    </stageInfo>

**Ожидаемый результат:**<br>
Статус извещения: "Подача ценовых предложений"
___

## 2. Работа комиссии (подведение итогов)
**Предусловие:**<br>
Шаблон: **epProtocolEF2020SubmitOffers.xml**<br>
TODO

    <id> - 8 цифр
    <externalId> - текст <externalId> исходящего файла 
    <versionNumber> - текст <versionNumber> исходящего файла 
    <commonInfo>
        <purchaseNumber> - текст <purchaseNumber> пакет epNotificationEF.xml !!!
    </commonInfo>
    <publishDTInETP> - текущая дата в исходном формате
    <procedureDT> - текущая дата в исходном формате
    <signDT> - текущая дата в исходном формате

**Ожидаемый результат:**<br>
Статус извещения: "Работа комиссии (подведение итогов)"
___

## 3. Заключение контракта
**Предусловие:**<br>
Шаблон: **epProtocolEF2020Final.xml**<br>
TODO

    <id> - 8 цифр
    <externalId> - текст <externalId> исходящего файла 
    <versionNumber> - текст <versionNumber> исходящего файла 
    <commonInfo>
        <purchaseNumber> - текст <purchaseNumber> пакет epNotificationEF.xml !!!
    </commonInfo>
    <publishDTInEIS> - текущая дата в исходном формате
    <publishDTInETP> - текущая дата в исходном формате
    <procedureDT> - текущая дата в исходном формате
    <signDT> - текущая дата в исходном формате

    <docDate> - все теги в шаблоне меняем на текущую дату в исходном формате

**Ожидаемый результат:**<br>
Статус контракта: "Заключение контракта"
___

</details>

<details><summary>Контракт. Публикация</summary>

**Предусловие:**<br>
Шаблон: **contract.xml**<br>
TODO

    <id> - 8 цифр
    <externalId> - текст <externalId> исходящего файла 
    <placementDate> - текущая дата в исходном формате
    <publishDate> - текст <publishDate> исходящего файла
    <foundation> - заменямем на тег <foundation> исходящего файла 
    <customer> - заменямем на тег <customer> исходящего файла 
    <placer> - заменямем на тег <placer> исходящего файла 
    <finances> - заменямем на тег <finances> исходящего файла 
    <protocolDate> - текст <protocolDate> исходящего файла 
    <documentCode> - 6 цифр
    <signDate> - текст <signDate> исходящего файла 
    <regNum> - текст <regNum> исходящего файла,  !!! если НЕТ: 19 цифр !!!
    <number> - текст <number> исходящего файла 
    <contractSubject> - текст <contractSubject> исходящего файла 
    <priceInfo> - заменямем на тег <finances> исходящего файла 
    <executionPeriod> - тега меняем на тег <executionPeriod> исходящего файла 
    <products> - тега меняем на тег <products> исходящего файла 
    <docDate> - все теги в шаблоне меняем на текущую дату в исходном формате

**Ожидаемый результат:**<br>
Статус контракта: "Исполнение контракта"
___
</details>

<details><summary>Контракт. Исполнение</summary>

**Предусловие:**<br>
Шаблон: **contract.xml**<br>
TODO

    <ns2:id> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <ns2:regNum> - текст тега меняем на текст тега <regNum> исходящего файла   
    <ns2:publishDate> - текст тега меняем на текущую дату в исходном формате
    <endDate> - текст тега меняем на текст тега <endDate> исходящего файла

    <fulfilledCost> - текст тега меняем на текст тега <fulfilledCost> исходящего файла   
    <docRegNumber> (все теги) - текст тега меняем на текст тега <regNum> исходящего файла   

    <docAcceptance> - меняеем текс теги у всех документов
        <sid> - добавить новый тег с текстом (любое число)
        <code> - текст тега меняем на текст тега <code> исходящего файла   
        <name> - текст тега меняем на текст тега <name> исходящего файла   
        <documentDate> - текст тега меняем на текст тега <documentDate> исходящего файла           
        <documentNum> - текст тега меняем на текст тега <documentNum> исходящего файла   
        <deliveryAcceptDate> - текст тега меняем на текст тега <deliveryAcceptDate> исходящего файла
    </docAcceptance> 

**Ожидаемый результат:**<br>
Статус контракта: "Исполнение контракта"
___
</details>

<details><summary>Отправка xml-пакета</summary>

    1. Авторизоваться на тестовом стенде по логину "Semenova1"
    2. В панели пользователя выбрать: Администрирование -> Контент -> Загрузка файлов во входящие
    3. Нажать кнопку "Выбрать и загрузить файл" и выбрать входящий файл

</details>

# Формирование XML пакетов 

<details><summary>Подтверждение</summary><br>

Шаблон: **confirmation.xml**

    <id> - 36 символов
    <loadId> - 8 цифр
    <refId> - текст <id> исходящего файла

</details>
<details><summary>Добавление новой позиции (или особой позиции) в опубликованный в ЕИС план-график</summary><br>

Шаблон: **tenderPlan2020.xml**

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
Статус плана-графика: "Идет отправка на контроль" -> "Опубликован в ЕИС"<br>
Статус позиции плана-графика: "Ожидает публикации в плане-графике ЕИС" -> "Включена в опубликованный в ЕИС план-график"


</details>

<details><summary>Формирование извещения</summary>
<details><summary>Электронный аукцион</summary>

### Подача ценовых предложений

Шаблон: **epNotificationEF.xml**

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
Статус извещение: "Подача ценовых предложений"


### Работа комиссии (подведение итогов)

Шаблон: **epProtocolEF2020SubmitOffers.xml**

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
Статус извещение: "Работа комиссии (подведение итогов)"

### Заключение контракта

Шаблон: **epProtocolEF2020Final.xml**

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
Статус извещение: "Заключение контракта"


</details>
</details>








<details><summary>Другое</summary>
# Исполнение контракта #

## 1. Стадия "Ожидание публикации (контракт)" ##

Исходящий файл: 3.xml (должен соответствовать схеме fcsIntegration.xsd)  
Входящий файл: 5975222_oosconfirm_xml.xml >!(должен соответствовать схеме fcsIntegration.xsd)

    Действия с тегами во входящем файле:

    Атрибуты "schemeVersion" тегов <data> входящего файла и <ext:data> исходящего файл должны быть одинаковые

    <id> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <createDateTime> - текст тега меняем на текущую дату в исходном формате
    <ns2:loadId> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <ns2:refId> - текст тега меняем на текст тега <ext:id> исходящего файла

    После внесения изменений входящий файл необходимо сохранить и отправить*!

### Ожидаемый результат: ###

Контракт находится в реестре: Исполнение -> Регистрация контрактов -> Контракты на этапе заключения  
Статус позиции: "Заключение контракта" -> "Ожидание публикации (контракт)"

## 2. Стадия "Исполнение контракта. Часть 1" ##

Исходящий файл: 3.xml (должен соответствовать схеме fcsIntegration.xsd)  
Входящий файл: contract_2780804383319000083_41655568_admin_1201 (должен соответствовать схеме fcsExport.xsd)

    Действия с тегами во входящем файле:

    Атрибуты "schemeVersion" тегов <ns2:epNotificationEF2020> входящего файла и <main:data> исходящего файл должны быть одинаковые

    <id> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <externalId> - текст тега меняем на текст тега <externalId> исходящего файла 
    <placementDate> - текст тега меняем на текущую дату в исходном формате
    <publishDate> - текст тега меняем на текст тега <publishDate> исходящего файла 
    <foundation> - тега меняем на тег <foundation> исходящего файла 
    <customer> - тега меняем на тег <customer> исходящего файла 
    <placer> - тега меняем на тег <placer> исходящего файла 
    <finances> - тега меняем на тег <finances> исходящего файла 
    <cmn:plan2020Number> - название тега меняем на <ns3:plan2020Number>
    <cmn:position2020Number> - название тега меняем на <ns3:position2020Number>
    <protocolDate> - текст тега меняем на текст тега <protocolDate> исходящего файла 
    <documentCode> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <signDate> - текст тега меняем на текст тега <signDate> исходящего файла 
    <regNum> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <number> - текст тега меняем на текст тега <number> исходящего файла 
    <contractSubject> - текст тега меняем на текст тега <contractSubject> исходящего файла 
    <priceInfo> - тега меняем на тег <finances> исходящего файла 
    <executionPeriod> - тега меняем на тег <executionPeriod> исходящего файла 
    <products> - тега меняем на тег <products> исходящего файла 
    <docRegNumber> - текст тега меняем на текст тега <regNum> входящего файла 
    <docRegNumber> - текст тега меняем на текст тега <regNum> входящего файла 
    <docRegNumber> - текст тега меняем на текст тега <regNum> входящего файла 

    После внесения изменений входящий файл необходимо сохранить и отправить*!

### Ожидаемый результат: ###

Контракт находится в реестре: Исполнение -> Реестр контрактов -> Контракты на этапе исполнения (последняя страница)  
Статус позиции: "Ожидание публикации (контракт)" -> "Исполнение контракта"

## 3. Стадия "Исполнение контракта. Часть 2" ##

Исходящий файл: 4.xml (должен соответствовать схеме fcsIntegration.xsd)  
Входящий файл: contractProcedure_2781148800721000013_181831266.xml (должен соответствовать схеме fcsExport.xsd)

    Действия с тегами во входящем файле:

    Атрибуты "schemeVersion" тегов <ns2:contractProcedure> входящего файла и <ext:data> исходящего файл должны быть одинаковые

    <ns2:id> - последние 4 цифры текста тега меняем на 4 случайные цифры
    <ns2:regNum> - текст тега меняем на текст тега <regNum> исходящего файла   
    <ns2:publishDate> - текст тега меняем на текущую дату в исходном формате
    <endDate> - текст тега меняем на текст тега <endDate> исходящего файла

    <fulfilledCost> - текст тега меняем на текст тега <fulfilledCost> исходящего файла   
    <docRegNumber> (все теги) - текст тега меняем на текст тега <regNum> исходящего файла   

    <executions>
        <execution>
            <docAcceptance> - меняеем текс теги у всех документов
                <sid> - добавить новый тег с текстом (любое число)
                <code> - текст тега меняем на текст тега <code> исходящего файла   
                <name> - текст тега меняем на текст тега <name> исходящего файла   
                <documentDate> - текст тега меняем на текст тега <documentDate> исходящего файла           
                <documentNum> - текст тега меняем на текст тега <documentNum> исходящего файла   
                <deliveryAcceptDate> - текст тега меняем на текст тега <deliveryAcceptDate> исходящего файла

    После внесения изменений входящий файл необходимо сохранить и отправить*!

### Ожидаемый результат: ###

Контракт находится в реестре: Исполнение -> Реестр контрактов -> Контракты на этапе исполнения (последняя страница)  
Статус позиции: "Ожидание публикации (контракт)" -> "Исполнение контракта"

***

#       * Отправка файла (пакета xml) #

    1. Авторизоваться на тестовом стенде по логину "Semenova1"
    2. В панели пользователя выбрать: Администрирование -> Контент -> Загрузка файлов во входящие
    3. Нажать кнопку "Выбрать и загрузить файл" и выбрать входящий файл
    4. Нажать кнопку "Принять и очистить"

#       Глоссарий тегов #

    <finalStageExecution> - закроет контракт (True/False)
    <regNum> - реестровый номер контракта (int)

</details>

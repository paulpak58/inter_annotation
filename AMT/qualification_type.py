import boto3
import xml.etree.ElementTree as ET

client = boto3.client('mturk',
     aws_access_key_id='AKIAXLGRKM3Q7C452FOS',
     aws_secret_access_key='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',
    region_name='us-east-1')
s3_url = ""

test_question = '''
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
<Overview>
    <Title>Open Annotation Protocol and Review Phases in Laparoscopic Cholecystectomy</Title>
    <Text>Please click the URL to access the Phase Annotation Protocol and review through the contents. After reading, confirm below.</Text>
</Overview>
<Question>
    <QuestionIdentifier>ReadAnnotationProtocol</QuestionIdentifier>
    <DisplayName>I have reviewed  the Annotation Protocol.</DisplayName>
    <IsRequired>true</IsRequired>
    <QuestionContent>
    <Text>Please confirm that you have read the contents of the Annotation Protocol and the IRB Agreement by selecting "Yes".</Text>
    <FormattedContent><![CDATA[<a href="">Annotation Protocol Guidelines</a>]]></FormattedContent>
    <FormattedContent><![CDATA[<a href="">IRB Agreement</a>]]></FormattedContent>
    </QuestionContent>
    <AnswerSpecification>
    <SelectionAnswer>
        <StyleSuggestion>radiobutton</StyleSuggestion>
        <Selections>
        <Selection>
            <SelectionIdentifier>Yes</SelectionIdentifier>
            <Text>Yes</Text>
        </Selection>
        <Selection>
            <SelectionIdentifier>No</SelectionIdentifier>
            <Text>No</Text>
        </Selection>
        </Selections>
    </SelectionAnswer>
    </AnswerSpecification>
</Question>
</QuestionForm>
'''


answer_text = '''
<AnswerKey xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/AnswerKey.xsd">
    <Question>
        <QuestionIdentifier>ReadAnnotationProtocol</QuestionIdentifier>
        <AnswerOption>
            <SelectionIdentifier>Yes</SelectionIdentifier>
            <AnswerScore>1</AnswerScore>
        </AnswerOption>
        <AnswerOption>
            <SelectionIdentifier>No</SelectionIdentifier>
            <AnswerScore>0</AnswerScore>
        </AnswerOption>
    </Question>
</AnswerKey>
'''


qualification_type_name = 'AnnotationProtocol'
response = client.list_qualification_types(Query=qualification_type_name, MustBeRequestable=False)
if response['NumResults'] > 0:
    qualification_type_id = response['QualificationTypes'][0]['QualificationTypeId']
    response = client.update_qualification_type(
        # Name='AnnotationProtocol',
        QualificationTypeId=qualification_type_id,
        Description='Please read and remember the definitions of start and endpoint of surgical phases in laparoscopic cholecystectomy and read the verbal IRB agreement form.',
        QualificationTypeStatus='Active',
        AutoGranted=False,
        # Keywords='video, classification, laparoscopic cholecystectomy, annotation, protocol',
        RetryDelayInSeconds=0, \
        # RetryDelayInSeconds=43200,              # 12 hours
        TestDurationInSeconds=3600,             # 1 hour
        Test=test_question,
        AnswerKey=answer_text
    )
else:
    # Qualification Type
    response = client.create_qualification_type(
        Name='AnnotationProtocol',
        Description='Please read and remember the definitions of start and endpoint of surgical phases in laparoscopic cholecystectomy and read the verbal IRB agreement form.',
        QualificationTypeStatus='Active',
        Keywords='video, classification, laparoscopic cholecystectomy, annotation, protocol',
        AutoGranted=False,
        RetryDelayInSeconds=0, \
        # RetryDelayInSeconds=43200,              # 12 hours
        TestDurationInSeconds=3600,             # 1 hour
        Test=test_question,
        AnswerKey=answer_text
    )
    print(response['QualificationType']['QualificationTypeId'])
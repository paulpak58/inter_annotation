import boto3
import xml.etree.ElementTree as ET

client = boto3.client('mturk',
     aws_access_key_id='AKIAXLGRKM3Q7C452FOS',
     aws_secret_access_key='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',
    region_name='us-east-1')
s3_url = "https://mghvideos.s3.us-east-2.amazonaws.com/Annotation+Protocol+AmTurk.pdf"

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
    <Text>Please confirm that you have read the contents of the Annotation Protocol by selecting "Yes".</Text>
    <FormattedContent><![CDATA[<a href="https://mghvideos.s3.us-east-2.amazonaws.com/Annotation+Protocol+AmTurk.pdf">Annotation Protocol PDF</a>]]></FormattedContent>
    </QuestionContent>
    <AnswerSpecification>
    <SelectionAnswer>
        <StyleSuggestion>radiobutton</StyleSuggestion>
        <Selections>
        <Selection>
            <SelectionIdentifier>Yes</SelectionIdentifier>
            <Text>Yes</Text>
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
    <QuestionIdentifier>read_google_drive_folder</QuestionIdentifier>
    <AnswerOption>
        <SelectionIdentifier>yes</SelectionIdentifier>
        <AnswerScore>1</AnswerScore>
    </AnswerOption>
    </Question>
</AnswerKey>
'''


# Qualification Type
response = client.create_qualification_type(
    Name='AnnotationProtocol',
    Description='Please read and remember the definitions of start and endpoint of surgical phases in laparoscopic cholecystectomy.',
    QualificationTypeStatus='Active',
    Keywords='video, classification, laparoscopic cholecystectomy, annotation, protocol',
    AutoGranted=False,
    RetryDelayInSeconds=86400,          # 24 hours
    TestDurationInSeconds=3600,             # 1 hour
    Test=test_question,
    AnswerKey=answer_text
)
print(response['QualificationType']['QualificationTypeId'])